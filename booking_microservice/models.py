"""SQLAlchemy models."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Booking(db.Model):  # type: ignore
    """Bookings model"""

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, nullable=False)
    publication_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    initial_date = db.Column(db.DateTime, nullable=False)
    final_date = db.Column(db.DateTime, nullable=False)
