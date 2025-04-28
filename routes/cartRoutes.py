from flask import Blueprint, request, redirect, session, url_for
from app import get_db_connection
from datetime import date

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    item_type = request.form.get('item_type')  # hotel / guide / destination
    item_id = int(request.form.get('item_id'))
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    trip_id = find_or_create_pending_trip(user_id)

    if item_type == 'hotel':
        add_hotel_to_trip(trip_id, item_id)
    elif item_type == 'guide':
        assign_guide_to_trip(trip_id, item_id)
    elif item_type == 'destination':
        add_activity_to_trip(trip_id, item_id)
    # elif item_type == 'transportation':
    #     add_transportation_to_trip(trip_id, item_id)
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
        WHERE Booking.UserID = %s AND CurrentStatus.IsCanceled = TRUE
        LIMIT 1
    """, (user_id,))
    result = cursor.fetchone()

    if result:
        trip_id = result['TripID']
    else:
        today = date.today()

        cursor.execute("CALL sp_add_trip_and_init_total(%s, %s, %s, %s, %s, %s)", (
            user_id,
            None,  # GuideID
            'My New Trip',
            today,
            today,
            'Auto created shopping cart trip'
        ))

        cursor2 = conn.cursor()
        cursor2.execute("SELECT LAST_INSERT_ID() AS NewTripID")
        row = cursor2.fetchone()
        trip_id = row['NewTripID']
        cursor2.close()

        cursor.execute("""
            SELECT StatusID FROM CurrentStatus WHERE IsCanceled = TRUE LIMIT 1
        """)
        status = cursor.fetchone()
        if not status:
            raise Exception('No Canceled StatusID found!')

        status_id = status['StatusID']

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
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Accommodation (TripID, HotelID, CheckInDate, CheckOutDate)
            VALUES (%s, %s, NULL, NULL)
        """, (trip_id, hotel_id))
        accommodation_id = cursor.lastrowid
        # add expense 0
        cursor.execute("""
        SELECT TotalExpenseID FROM TotalExpense WHERE TripID = %s
        """, (trip_id,))
        total_expense = cursor.fetchone()
        if total_expense:
            cursor.execute("""
                INSERT INTO AccommodationExpense (AccommodationID, TotalExpenseID, Amount, ExpenseDescription)
                VALUES (%s, %s, 0, %s)
            """, (accommodation_id, total_expense['TotalExpenseID'], 'Accommodation Expense'))
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def assign_guide_to_trip(trip_id, guide_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Trip
            SET GuideID = %s
            WHERE TripID = %s
        """, (guide_id, trip_id))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def add_activity_to_trip(trip_id, destination_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Chck if destination exists
        cursor.execute("""
            SELECT City FROM Destination WHERE DestinationID = %s
        """, (destination_id,))
        destination = cursor.fetchone()
        if not destination:
            raise Exception('Destination not found!')

        activity_name = f'{destination['City']} - Auto generated activity'

        # Check if trip exists
        cursor.execute("""
            SELECT TripID FROM Trip WHERE TripID = %s
        """, (trip_id,))
        trip = cursor.fetchone()
        if not trip:
            raise Exception('Trip not found!')

        # Check if activity already exists
        cursor.execute("""
            INSERT INTO Activity (TripID, DestinationID, ActivityName, ActivityDescription, StartDate, Duration)
            VALUES (%s, %s, %s, %s, NULL, NULL)
        """, (trip_id, destination_id, activity_name, 'Auto generated activity'))

        activity_id = cursor.lastrowid
        # add expense 0
        cursor.execute("""
            SELECT TotalExpenseID FROM TotalExpense WHERE TripID = %s
        """, (trip_id,))
        total_expense = cursor.fetchone()
        if total_expense:
            cursor.execute("""
                INSERT INTO ActivityExpense (ActivityID, TotalExpenseID, Amount, ExpenseDescription)
                VALUES (%s, %s, 0, %s)
            """, (activity_id, total_expense['TotalExpenseID'], 'Activity Expense'))
            
        conn.commit()

    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        raise e
    finally:
        cursor.close()
        conn.close()
