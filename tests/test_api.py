"""Sample test suite."""

import json
import logging
import tempfile

# pylint:disable=redefined-outer-name,protected-access
import pytest

from booking_microservice.app import create_app
from booking_microservice.models import db

logger = logging.getLogger(__name__)


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


@pytest.fixture
def booking():
    return {
        "tenant_id": 1,
        "publication_id": 1,
        "total_price": 10,
        "initial_date": "2021-02-22",
        "final_date": "2021-02-24",
    }


def test_booking(client, booking):
    response = client.post("/v1/bookings", json=booking)
    assert response._status_code == 201
    new_booking = json.loads(response.data)
    assert new_booking.get("booking_status") == "PENDING"
    assert new_booking.get("blockchain_status") == "UNSET"
    assert new_booking.get("blockchain_transaction_hash") is None
    assert new_booking.get("blockchain_id") is None


def test_get_booking(client, booking):
    response = client.post("/v1/bookings", json=booking)
    assert response._status_code == 201
    response = client.get("/v1/bookings?blockchain_status=UNSET")
    assert response._status_code == 200
    assert len(json.loads(response.data)) == 1


def test_get_booking_patch_blockchain_status(client, booking):
    _ = client.post("/v1/bookings", json=booking)
    response = client.patch("/v1/bookings/1", json={"blockchain_status": "PENDING"})
    patched_booking = json.loads(response.data)
    assert patched_booking.get("blockchain_status") == "PENDING"
    assert patched_booking.get("blockchain_transaction_hash") is None
    assert patched_booking.get("blockchain_id") is None
    assert patched_booking.get("booking_status") == "PENDING"


def test_get_booking_patch_blockchain_transaction_hash(client, booking):
    _ = client.post("/v1/bookings", json=booking)
    response = client.patch(
        "/v1/bookings/1", json={"blockchain_transaction_hash": "0x0BADBEEF"}
    )
    patched_booking = json.loads(response.data)
    assert patched_booking.get("blockchain_status") == "UNSET"
    assert patched_booking.get("blockchain_transaction_hash") == "0x0BADBEEF"
    assert patched_booking.get("blockchain_id") is None
    assert patched_booking.get("booking_status") == "PENDING"


def test_get_booking_patch_blockchain_id(client, booking):
    _ = client.post("/v1/bookings", json=booking)
    response = client.patch("/v1/bookings/1", json={"blockchain_id": 12345678})
    patched_booking = json.loads(response.data)
    assert patched_booking.get("blockchain_status") == "UNSET"
    assert patched_booking.get("blockchain_transaction_hash") is None
    assert patched_booking.get("blockchain_id") == 12345678
    assert patched_booking.get("booking_status") == "PENDING"


def test_get_booking_patch_booking_status(client, booking):
    _ = client.post("/v1/bookings", json=booking)
    response = client.patch("/v1/bookings/1", json={"booking_status": "ACCEPTED"})
    patched_booking = json.loads(response.data)
    assert patched_booking.get("blockchain_status") == "UNSET"
    assert patched_booking.get("blockchain_transaction_hash") is None
    assert patched_booking.get("blockchain_id") is None
    assert patched_booking.get("booking_status") == "ACCEPTED"
