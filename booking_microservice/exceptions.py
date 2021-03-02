"""Custom exceptions."""


class BookingDoesNotExist(Exception):
    pass


class ServerTokenError(Exception):
    pass


class UnsetServerToken(Exception):
    pass
