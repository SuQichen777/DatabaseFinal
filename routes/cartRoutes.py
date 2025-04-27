from flask import Blueprint, request, redirect, session, url_for
from app import get_db_connection
from datetime import date

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    item_type = request.form.get('item_type')  # hotel / guide / destination / transportation
    item_id = int(request.form.get('item_id'))
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    trip_id = find_or_create_pending_trip(user_id)

    if item_type == 'hotel':
        add_hotel_to_trip(trip_id, item_id)
    elif item_type == 'guide':
        assign_guide_to_trip(trip_id, item_id)
    elif item_type == 'destination':
        add_activity_to_trip(trip_id, item_id)
    elif item_type == 'transportation':
        add_transportation_to_trip(trip_id, item_id)
    else:
        return "Invalid item type", 400

    return redirect(request.referrer or url_for('trips.trips_home'))

def find_or_create_pending_trip(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TripID
        FROM Booking
        JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
        WHERE Booking.UserID = %s AND CurrentStatus.IsPending = TRUE
        LIMIT 1
    """, (user_id,))
    result = cursor.fetchone()

    if result:
        trip_id = result['TripID']
    else:
        cursor.execute("""
            INSERT INTO Trip (UserID, TripName, TripDes)
            VALUES (%s, %s, %s)
        """, (user_id, 'My New Trip', 'Auto created shopping cart trip'))
        trip_id = cursor.lastrowid


        cursor.execute("""
            SELECT StatusID FROM CurrentStatus WHERE IsPending = TRUE LIMIT 1
        """)
        status = cursor.fetchone()
        if not status:
            raise Exception('No Pending StatusID found!')

        status_id = status['StatusID']

        today = date.today()
        cursor.execute("""
            INSERT INTO Booking (StatusID, UserID, TripID, BookingDate)
            VALUES (%s, %s, %s, %s)
        """, (status_id, user_id, trip_id, today))

    conn.commit()
    cursor.close()
    conn.close()
    return trip_id

def add_hotel_to_trip(trip_id, hotel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    today = date.today()
    tomorrow = date.fromordinal(today.toordinal() + 1)

    cursor.execute("""
        INSERT INTO Accommodation (TripID, HotelID, CheckInDate, CheckOutDate)
        VALUES (%s, %s, %s, %s)
    """, (trip_id, hotel_id, today, tomorrow))

    conn.commit()
    cursor.close()
    conn.close()

def assign_guide_to_trip(trip_id, guide_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Trip
        SET GuideID = %s
        WHERE TripID = %s
    """, (guide_id, trip_id))

    conn.commit()
    cursor.close()
    conn.close()

def add_activity_to_trip(trip_id, destination_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    today = date.today()

    cursor.execute("""
        INSERT INTO Activity (TripID, DestinationID, ActivityName, ActivityDescription, StartDate, Duration)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (trip_id, destination_id, 'Default Activity', 'Auto generated activity', today, 1))

    conn.commit()
    cursor.close()
    conn.close()

def add_transportation_to_trip(trip_id, transportation_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Transportation WHERE TransportationID = %s
    """, (transportation_id,))
    transportation = cursor.fetchone()

    if not transportation:
        raise Exception('Transportation not found!')

    cursor.execute("""
        INSERT INTO Transportation (TripID, StartDate, Duration, StartingPoint, EndingPoint, TransportationType)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        trip_id,
        transportation[2],  # StartDate
        transportation[3],  # Duration
        transportation[4],  # StartingPoint
        transportation[5],  # EndingPoint
        transportation[6],  # TransportationType
    ))

    conn.commit()
    cursor.close()
    conn.close()
