"""Metrics test suite."""

import json
import logging
import tempfile
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td

# pylint:disable=redefined-outer-name,protected-access
import pytest

from booking_microservice.app import create_app
from booking_microservice.constants import BlockChainStatus, BookingStatus
from booking_microservice.models import db

logger = logging.getLogger(__name__)


@pytest.fixture
def booking():
    return {
        "tenant_id": 1,
        "publication_id": 1,
        "total_price": 10,
        "initial_date": "2021-02-14",
        "final_date": "2021-02-20",
    }


@pytest.fixture
def client():
    with tempfile.NamedTemporaryFile() as dbf:
        app = create_app(test_db=f"sqlite:///{dbf.name}")
        with app.app_context():
            from flask_migrate import upgrade as _upgrade

            _upgrade()
        with app.test_client() as test_client:
            yield test_client
        with app.app_context():
            db.drop_all()


def test_revenue_per_day(client, booking):
    r = client.post("/v1/bookings", json=booking)
    booking = json.loads(r.data)
    client.patch(
        f"/v1/bookings/{booking.get('id')}",
        json={
            "booking_status": BookingStatus.ACCEPTED.value,
            "blockchain_status": BlockChainStatus.CONFIRMED.value,
        },
    )
    r = client.get(
        "/v1/metrics",
        data={
            "start_date": dt.utcnow().date().isoformat(),
            "end_date": dt.utcnow().date().isoformat(),
        },
    )
    assert r._status_code == 200
    assert json.loads(r.data) == [
        {
            "name": "revenue_per_day",
            "data": [
                {
                    "date": dt.utcnow().date().isoformat(),
                    "value": booking.get("total_price") * 1.0,
                }
            ],
        }
    ]


def test_revenue_per_day_tenfold(client, booking):
    for i in range(10):
        week_booking = dict(booking)
        week_booking["initial_date"] = (
            date.fromisoformat(booking["initial_date"]) + td(days=i)
        ).isoformat()

        week_booking["final_date"] = (
            date.fromisoformat(booking["initial_date"]) + td(days=i)
        ).isoformat()

        r = client.post("/v1/bookings", json=week_booking)
        assert r._status_code == 201
        new_booking = json.loads(r.data)
        client.patch(
            f"/v1/bookings/{new_booking.get('id')}",
            json={
                "booking_status": BookingStatus.ACCEPTED.value,
                "blockchain_status": BlockChainStatus.CONFIRMED.value,
            },
        )
    r = client.get(
        "/v1/metrics",
        data={
            "start_date": dt.utcnow().date().isoformat(),
            "end_date": dt.utcnow().date().isoformat(),
        },
    )
    assert r._status_code == 200
    assert json.loads(r.data) == [
        {
            "name": "revenue_per_day",
            "data": [
                {
                    "date": dt.utcnow().date().isoformat(),
                    "value": booking.get("total_price") * 10.0,
                }
            ],
        }
    ]


def test_revenue_per_day_2(client, booking):
    r = client.post("/v1/bookings", json=booking)
    booking = json.loads(r.data)
    client.patch(
        f"/v1/bookings/{booking.get('id')}",
        json={
            "booking_status": BookingStatus.ACCEPTED.value,
            "blockchain_status": BlockChainStatus.CONFIRMED.value,
        },
    )
    r = client.get(
        "/v1/metrics",
        data={
            "start_date": dt.utcnow().date().isoformat(),
            "end_date": (dt.utcnow() + td(days=1)).date().isoformat(),
        },
    )
    assert r._status_code == 200
    assert json.loads(r.data) == [
        {
            "name": "revenue_per_day",
            "data": [
                {
                    "date": dt.utcnow().date().isoformat(),
                    "value": booking.get("total_price") * 1.0,
                },
                {"date": (dt.utcnow() + td(days=1)).date().isoformat(), "value": 0.0},
            ],
        }
    ]


def test_revenue_per_day_3(client, booking):
    r = client.post("/v1/bookings", json=booking)
    booking = json.loads(r.data)
    client.patch(
        f"/v1/bookings/{booking.get('id')}",
        json={
            "booking_status": BookingStatus.ACCEPTED.value,
            "blockchain_status": BlockChainStatus.CONFIRMED.value,
        },
    )
    r = client.get(
        "/v1/metrics",
        data={
            "start_date": (dt.utcnow() - td(days=1)).date().isoformat(),
            "end_date": dt.utcnow().date().isoformat(),
        },
    )
    assert r._status_code == 200
    assert json.loads(r.data) == [
        {
            "name": "revenue_per_day",
            "data": [
                {"date": (dt.utcnow() - td(days=1)).date().isoformat(), "value": 0.0},
                {
                    "date": dt.utcnow().date().isoformat(),
                    "value": booking.get("total_price") * 1.0,
                },
            ],
        }
    ]


def test_revenue_per_day_4(client, booking):
    r = client.post("/v1/bookings", json=booking)
    booking = json.loads(r.data)
    client.patch(
        f"/v1/bookings/{booking.get('id')}",
        json={
            "booking_status": BookingStatus.ACCEPTED.value,
            "blockchain_status": BlockChainStatus.CONFIRMED.value,
        },
    )
    r = client.get(
        "/v1/metrics",
        data={
            "start_date": (dt.utcnow() - td(days=1)).date().isoformat(),
            "end_date": (dt.utcnow() + td(days=1)).date().isoformat(),
        },
    )
    assert r._status_code == 200
    assert json.loads(r.data) == [
        {
            "name": "revenue_per_day",
            "data": [
                {"date": (dt.utcnow() - td(days=1)).date().isoformat(), "value": 0.0},
                {
                    "date": dt.utcnow().date().isoformat(),
                    "value": booking.get("total_price") * 1.0,
                },
                {"date": (dt.utcnow() + td(days=1)).date().isoformat(), "value": 0.0},
            ],
        }
    ]
