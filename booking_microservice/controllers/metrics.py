"""Metrics controller."""
from datetime import timedelta as td

from sqlalchemy import func

from booking_microservice.constants import BlockChainStatus, BookingStatus
from booking_microservice.models import Booking


def prepare(name, query, cols):
    return {"name": name, "data": [dict(zip(cols, r)) for r in query]}


def pad(metric, start_date, end_date):
    dates = [d.get("date") for d in metric.get("data")]

    current_date = start_date

    while current_date <= end_date:
        if current_date.isoformat() not in dates:
            metric["data"].append({"date": current_date.isoformat(), "value": 0})
        current_date += td(days=1)

    metric["data"] = sorted(metric["data"], key=lambda x: x.get("date"))

    return metric


def revenue_per_day(start_date, end_date):
    count = (
        Booking.query.filter(
            (func.date(Booking.booking_date).between(start_date, end_date))
            & (Booking.booking_status == BookingStatus.ACCEPTED.value)
            & (Booking.blockchain_status == BlockChainStatus.CONFIRMED.value)
        )
        .with_entities(
            func.date(Booking.booking_date),
            func.sum(Booking.total_price),
            func.count(Booking.id),
        )
        .group_by(func.date(Booking.booking_date))
        .order_by(func.date(Booking.booking_date))
        .all()
    )
    metric = prepare("revenue_per_day", count, ["date", "value"])
    metric = pad(metric, start_date, end_date)
    return metric


all_metrics = [revenue_per_day]
