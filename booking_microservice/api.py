"""API module."""
from flask_restx import Api, Resource, fields
from booking_microservice.models import Booking, db

api = Api(
    prefix="/v1",
    title="Bookings API",
    description="Bookings microservice for BookBNB",
    default="Bookings",
    default_label="Bookings operations",
)

booking_model = api.model(
    'Booking',
    {
        "booking_id": fields.Integer(
            required=True, description="The unique identifier of the booking"
        ),
        "tenant_id": fields.Integer(
            required=True, description="The unique identifier of the tenant"
        ),
        "room_id": fields.Integer(
            required=True, description="The unique identifier of the rented room"
        ),
        "total_price": fields.Float(
            required=True, description="The total price of the operation",
        ),
        "initial_date": fields.DateTime(
            required=True, description="The starting date of the rental",
        ),
        "final_date": fields.DateTime(
            required=True, description="The final date of the rental"
        ),
    },
)


@api.route('/booking')
class BookingListResource(Resource):
    @api.doc('list_bookings')
    @api.marshal_with(booking_model, as_list=True)
    def get(self):
        """Get all bookings."""
        return Booking.query.all()

    @api.doc('create_booking')
    @api.expect(booking_model, validate=True)
    @api.marshal_with(booking_model)
    def post(self):
        """Create a new booking"""
        new_booking = Booking(**api.payload)
        db.session.add(new_booking)
        db.session.commit()
        return new_booking


@api.route('/booking/roomrentals/<int:room_id>')
@api.response(404, 'Invalid room id')
class BookingRoomRentalsListResource(Resource):
    @api.doc('get_room_id_rentals')
    @api.marshal_with(booking_model, as_list=True)
    def get(self, room_id):
        """Get all bookings by room id."""
        rentals = Booking.query.filter(Booking.room_id == room_id).all()
        return rentals
