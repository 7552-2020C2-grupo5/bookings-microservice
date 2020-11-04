"""SQLAlchemy models."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Booking(db.Model):  # type: ignore
    """Bookings model"""

    booking_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    initial_date = db.Column(db.DateTime)
    final_date = db.Column(db.DateTime)
