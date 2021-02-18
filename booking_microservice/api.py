"""API module."""
import operator as ops
from datetime import datetime as dt

from flask_restx import Api, Resource, fields, reqparse

from booking_microservice import __version__
from booking_microservice.constants import BlockChainStatus
from booking_microservice.exceptions import BookingDoesNotExist
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


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)


@api.errorhandler(BookingDoesNotExist)
def handle_publication_does_not_exist(_error: BookingDoesNotExist):
    """Handle non-existing booking exception."""
    return {'message': "No booking by that id was found."}, 404


new_booking_model = api.model(
    'New Booking',
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

booking_patch_model = api.model(
    "Booking patch",
    {
        "blockchain_status": fields.String(
            required=True,
            description="The status on the blockchain",
            enum=[x.value for x in BlockChainStatus],
            default=BlockChainStatus.UNSET.value,
            attribute='blockchain_status.value',
        ),
        "blockchain_transaction_hash": fields.String(
            required=False, description="The hash of the transaction on the blockchain"
        ),
        "blockchain_id": fields.Integer(
            required=False, description="The id on the blockchain"
        ),
    },
)


booking_model = api.inherit(
    "Created booking",
    new_booking_model,
    {
        "blockchain_status": fields.String(
            required=True,
            description="The status on the blockchain",
            enum=[x.value for x in BlockChainStatus],
            default=BlockChainStatus.UNSET.value,
            attribute='blockchain_status.value',
        ),
        "blockchain_transaction_hash": fields.String(
            required=False, description="The hash of the transaction on the blockchain"
        ),
        "blockchain_id": fields.Integer(
            required=False, description="The id on the blockchain"
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
bookings_parser.add_argument(
    "blockchain_status",
    type=FilterParam("blockchain_status", ops.eq, schema=str),
    help="blockchain_status",
    default=BlockChainStatus.CONFIRMED.value,
)
bookings_parser.add_argument(
    "blockchain_transaction_hash",
    type=FilterParam("blockchain_transaction_hash", ops.eq),
    help="Hash of the transaction that inserted the booking into the blockchain",
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
    @api.expect(new_booking_model)
    @api.response(code=201, model=booking_model, description="Success")
    @api.response(code=412, model=error_model, description="Precondition Failed")
    def post(self):
        """Create a new booking"""
        data = api.payload
        data["initial_date"] = dt.fromisoformat(data["initial_date"]).date()
        data["final_date"] = dt.fromisoformat(data["final_date"]).date()

        initial_date = data["initial_date"]
        final_date = data["final_date"]
        publication_id = data["publication_id"]

        overlapped_bookings = Booking.query.filter(
            (Booking.initial_date <= final_date)
            & (Booking.final_date >= initial_date)
            & (Booking.publication_id == publication_id)
        ).all()

        if len(overlapped_bookings) >= 1:
            return {"message": "The intent booking has overlapping dates"}, 412

        new_booking = Booking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return api.marshal(new_booking, booking_model), 201


@api.route("/bookings/<int:booking_id>")
class BookingResource(Resource):
    @api.doc("patch_booking")
    @api.expect(booking_patch_model)
    @api.marshal_with(booking_model)
    def patch(self, booking_id):
        """Replace a booking by id."""
        booking = Booking.query.filter(Booking.id == booking_id).first()
        if booking is None:
            raise BookingDoesNotExist

        data = api.payload

        booking.update_from_dict(**data)
        db.session.merge(booking)
        db.session.commit()
        return booking
