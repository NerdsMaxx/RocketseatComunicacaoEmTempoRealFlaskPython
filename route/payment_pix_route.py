from flask import Blueprint, jsonify, request, send_file, render_template
from datetime import datetime, timedelta
from model.entity.payment import Payment
from model.payments.pix import Pix
from repository.database import db
from websocket.socketio import socketio

payment_pix_bp = Blueprint(
    'payment_pix_routes',
    __name__,
    url_prefix='/payments/pix')

@payment_pix_bp.post('')
def create_payment_pix():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({'message': 'Invalid value'}), 400

    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'], expiration_date=expiration_date)

    result = Pix().create_payment()

    new_payment.bank_payment_id = result.bank_payment_id
    new_payment.qr_code = result.qr_code_path

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({'message': 'The payment has been created',
                    'payment': new_payment.to_dict()})

@payment_pix_bp.get('/qr_code/<file_name>')
def get_image(file_name):
    return send_file(f'static/img/{file_name}.png', mimetype='image/png')

@payment_pix_bp.post('/confirmation')
def pix_confirmation():
    data = request.get_json()

    if 'bank_payment_id' not in data or 'value' not in data:
        return jsonify({'message': 'Invalid payment data'}), 400

    bank_payment_id = data.get('bank_payment_id')
    payment: Payment = Payment.query.filter_by(bank_payment_id = bank_payment_id).first()

    if not payment or payment.paid:
        return jsonify({'message': 'Payment not found'}), 404

    if data.get('value') != payment.value:
        return jsonify({'message': 'Invalid payment data'}), 400

    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}')

    return jsonify({'message': 'The payment has been confirmed'})

@payment_pix_bp.get('/<int:payment_id>')
def payment_pix_page(payment_id: int):
    payment: Payment = Payment.query.get(payment_id)

    if not payment:
        return render_template('404.html')

    if payment.paid:
        return render_template('confirmed_payment.html',
                               payment_id=payment.id,
                               value=payment.value)

    return render_template('payment.html',
                           payment_id = payment.id,
                           value = payment.value,
                           host = 'http://127.0.0.1:5000',
                           qr_code = payment.qr_code)

# websockets


