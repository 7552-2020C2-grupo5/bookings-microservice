"""Constant values and defaults used in multiple modules."""
from enum import Enum


class BlockChainStatus(Enum):
    UNSET = "UNSET"
    CONFIRMED = "CONFIRMED"
    DENIED = "DENIED"
    PENDING = "PENDING"
    ERROR = "ERROR"


class BookingStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


DEFAULT_VERIFICATION_URL = (
    "https://tokens-microservice.herokuapp.com/v1/tokens/verification"
)
