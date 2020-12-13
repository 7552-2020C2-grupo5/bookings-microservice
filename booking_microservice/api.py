"""API module."""
from datetime import datetime as dt
from flask_restx import Api, Resource, fields, reqparse
from booking_microservice.models import Booking, db
from booking_microservice.utils import FilterParam
import operator as ops
from booking_microservice import __version__

api = Api(
    prefix="/v1",
    version=__version__,
    title="Bookings API",
    description="Bookings microservice for BookBNB",
    default="Bookings",
    default_label="Bookings operations",
    validate=True,
)

booking_model = api.model(
    'Booking',
    {
        "id": fields.Integer(
            readonly=True, description="The unique identifier of the booking",
        ),
        "tenant_id": fields.Integer(
            required=True, description="The unique identifier of the tenant"
        ),
        "publication_id": fields.Integer(
            required=True, description="The unique identifier of the publication"
        ),
        "total_price": fields.Float(
            required=True, description="The total price of the operation",
        ),
        "initial_date": fields.Date(
            required=True, description="The starting date of the rental",
        ),
        "final_date": fields.Date(
            required=True, description="The final date of the rental"
        ),
        "booking_date": fields.DateTime(
            readonly=True, description="Date the booking was created"
        ),
    },
)

bookings_parser = reqparse.RequestParser()
bookings_parser.add_argument(
    "tenant_id",
    type=FilterParam("tenant_id", ops.eq, schema="int"),
    help="id of tenant",
    store_missing=False,
)
bookings_parser.add_argument(
    "publication_id",
    type=FilterParam("publication_id", ops.eq, schema="int"),
    help="id of publication",
    store_missing=False,
)
# TODO: filter initial date
# TODO: filter final date
# TODO: filter creation date


@api.route('/bookings')
class BookingListResource(Resource):
    @api.doc('list_bookings')
    @api.marshal_list_with(booking_model)
    @api.expect(bookings_parser)
    def get(self):
        """Get all bookings."""
        params = bookings_parser.parse_args()
        query = Booking.query
        for _, filter_op in params.items():
            query = filter_op.apply(query, Booking)
        return query.all()

    @api.doc('create_booking')
    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def post(self):
        """Create a new booking"""
        data = api.payload
        data["initial_date"] = dt.fromisoformat(data["initial_date"]).date()
        data["final_date"] = dt.fromisoformat(data["final_date"]).date()
        new_booking = Booking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return new_booking
