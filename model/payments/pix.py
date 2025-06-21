import uuid
from dataclasses import dataclass

import qrcode


class Pix:
    def __init__(self):
        pass

    def create_payment(self, base_dir = ''):
        # criar o pagamento na instituicao financeira
        bank_payment_id = uuid.uuid4()

        # gerar hash
        hash_payment = f'hash_payment_{bank_payment_id}'

        # qr code
        img = qrcode.make(hash_payment)
        img.save(f'{base_dir}static/img/qr_code_payment_{bank_payment_id}.png')

        return PixResult(bank_payment_id, f'qr_code_payment_{bank_payment_id}')

@dataclass(frozen=True)
class PixResult:
    bank_payment_id: uuid.UUID
    qr_code_path: str