"""API module."""
import operator as ops
from datetime import datetime as dt

from flask_restx import Api, Resource, fields, reqparse

from booking_microservice import __version__
from booking_microservice.models import Booking, db
from booking_microservice.utils import FilterParam

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
bookings_parser.add_argument(
    "initial_date",
    type=FilterParam(
        "initial_date",
        ops.ge,
        schema="date",
        format_="date",
        transform=dt.fromisoformat,
    ),
    help="minimum starting date",
    store_missing=False,
)
bookings_parser.add_argument(
    "final_date",
    type=FilterParam(
        "final_date", ops.le, schema="date", format_="date", transform=dt.fromisoformat,
    ),
    help="maximum final date",
    store_missing=False,
)
bookings_parser.add_argument(
    "booking_date",
    type=FilterParam(
        "booking_date",
        ops.eq,
        schema="date",
        format_="date",
        transform=dt.fromisoformat,
    ),
    help="booking date",
    store_missing=False,
)

error_model = api.model(
    "Bookings error model",
    {"message": fields.String(description="A message describing the error")},
)


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
    @api.response(code=201, model=booking_model, description="Success")
    @api.response(code=412, model=error_model, description="Precondition Failed")
    def post(self):
        """Create a new booking"""
        data = api.payload
        data["initial_date"] = dt.fromisoformat(data["initial_date"]).date()
        data["final_date"] = dt.fromisoformat(data["final_date"]).date()

        initial_date = data["initial_date"]
        final_date = data["final_date"]

        overlapped_bookings = Booking.query.filter(
            (Booking.initial_date <= final_date) & (Booking.final_date >= initial_date)
        ).all()

        if len(overlapped_bookings) >= 1:
            return {"message": "The intent booking has overlapping dates"}, 412

        new_booking = Booking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return api.marshal(new_booking, booking_model), 201
