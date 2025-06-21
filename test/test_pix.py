import sys
sys.path.append("../")

import pytest
import os
from model.payments.pix import Pix

def test_pix_create_payment():
    pix_instance = Pix()

    # create a payment
    payment_info = pix_instance.create_payment(base_dir='../')

    assert payment_info is not None
    assert payment_info.bank_payment_id is not None
    assert payment_info.qr_code_path is not None

    path = f'../static/img/{payment_info.qr_code_path}.png'
    os.path.isfile(path)

    os.remove(path)
