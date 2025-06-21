from datetime import datetime
from uuid import UUID

import sqlalchemy
from sqlalchemy import Float, Boolean, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from repository.database import db

class Payment(db.Model):
    # id, value, paid, bank_payment_id, qr_code, expiration_date
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    bank_payment_id: Mapped[UUID] = mapped_column(String(36), nullable=True)
    qr_code: Mapped[str] = mapped_column(String(200), nullable=True)
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'paid': self.paid,
            'bank_payment_id': self.bank_payment_id,
            'qr_code': self.qr_code,
            'expiration_date': self.expiration_date
        }