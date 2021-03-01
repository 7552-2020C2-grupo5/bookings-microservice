"""API module."""
from flask_restx import Api

from booking_microservice import __version__
from booking_microservice.namespaces.bookings import api as bookings_namespace
from booking_microservice.namespaces.metrics import api as metrics_namespace
from booking_microservice.namespaces.token import api as token_namespace

api = Api(
    prefix="/v1",
    version=__version__,
    title="Bookings API",
    description="Bookings microservice for BookBNB",
    default="Bookings",
    default_label="Bookings operations",
    validate=True,
)
api.add_namespace(bookings_namespace, path='/bookings')
api.add_namespace(metrics_namespace, path='/metrics')
api.add_namespace(token_namespace, path='/token')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)
