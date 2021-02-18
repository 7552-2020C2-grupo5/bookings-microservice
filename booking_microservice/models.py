"""SQLAlchemy models."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from booking_microservice.constants import BlockChainStatus

db = SQLAlchemy()


class Booking(db.Model):  # type: ignore
    """Bookings model"""

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, nullable=False)
    publication_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    initial_date = db.Column(db.Date, nullable=False)
    final_date = db.Column(db.Date, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=func.now())
    blockchain_status = db.Column(
        db.Enum(BlockChainStatus), nullable=False, default=BlockChainStatus.UNSET.value,
    )
    blockchain_transaction_hash = db.Column(db.String(512), nullable=True)
    blockchain_id = db.Column(db.Integer, nullable=True)

    def update_from_dict(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
