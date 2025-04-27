from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app import get_db_connection
from datetime import date, timedelta



trips_bp = Blueprint('trips', __name__, url_prefix='/trips')
destination_bp = Blueprint('destination', __name__, url_prefix='/destination')
tour_guide_bp = Blueprint('tour_guide', __name__, url_prefix='/tour_guide')
hotel_bp = Blueprint('hotel', __name__, url_prefix='/hotel')
transportation_bp = Blueprint('transportation', __name__, url_prefix='/transportation')

# Trips Homepage
@trips_bp.route('/', methods=['GET'])
def trips_home():
    search_query = request.args.get('search', '')
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("CALL sp_get_visible_trips(%s, %s)", (user_id, search_query))
    trips = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/trips.html', trips=trips, search_query=search_query)

# Trip Detail Page

def generate_days(start_date, end_date):
    """Generate list of dates between start and end (inclusive)."""
    days = []
    current = start_date
    while current <= end_date:
        days.append(current)
        current += timedelta(days=1)
    return days

@trips_bp.route('/<int:trip_id>', methods=['GET'])
def trip_detail(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Trip.*, 
            Trip.UserID AS TripOwnerID,
            Booking.UserID AS BookingUserID, 
            CurrentStatus.IsConfirmed, CurrentStatus.IsPending, CurrentStatus.IsCanceled,
            Guide.GuideName,
            Users.Name AS OwnerName
        FROM Trip
        LEFT JOIN Booking ON Trip.TripID = Booking.TripID
        LEFT JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
        LEFT JOIN Guide ON Trip.GuideID = Guide.GuideID
        LEFT JOIN Users ON Trip.UserID = Users.UserID
        WHERE Trip.TripID = %s
    """, (trip_id,))
    trip = cursor.fetchone()

    if not trip:
        cursor.close()
        conn.close()
        flash('Trip not found.', 'danger')
        return redirect(url_for('trips.trips_home'))

    is_owner = (trip['TripOwnerID'] == user_id)
    can_edit = is_owner and trip['IsCanceled']  # Only when public-cancelled and is owner can edit
    is_visible = is_owner or trip['IsConfirmed']

    if not is_visible:
        cursor.close()
        conn.close()
        flash('You are not allowed to view this Trip.', 'danger')
        return redirect(url_for('trips.trips_home'))

    scheduled_items = []
    unscheduled_items = []

    # Fetch activities, accommodations, and transportations which are already scheduled
    cursor.callproc('sp_get_activities_by_trip', (trip_id,))
    activities = cursor.fetchall()
    cursor.nextset()

    cursor.callproc('sp_get_accommodations_by_trip', (trip_id,))
    accommodations = cursor.fetchall()
    cursor.nextset()

    cursor.callproc('sp_get_transportations_by_trip', (trip_id,))
    transportations = cursor.fetchall()
    cursor.nextset()

    # Fetch activities, accommodations, and transportations which are not scheduled
    cursor.callproc('sp_get_unscheduled_activities', (trip_id,))
    unscheduled_activities = cursor.fetchall()
    cursor.nextset()

    cursor.callproc('sp_get_unscheduled_accommodations', (trip_id,))
    unscheduled_accommodations = cursor.fetchall()
    cursor.nextset()

    cursor.callproc('sp_get_unscheduled_transportations', (trip_id,))
    unscheduled_transportations = cursor.fetchall()
    cursor.nextset()

    # Fetch total expense
    cursor.callproc('sp_get_total_expense_by_trip', (trip_id,))
    total_expense = cursor.fetchone()
    cursor.nextset()

    # Fetch reviews if not the owner
    reviews = []
    if not is_owner:
        cursor.callproc('sp_get_reviews_by_trip', (trip_id,))
        reviews = cursor.fetchall()
        cursor.nextset()
    # For other's trip, generate related trip
    cursor.callproc('sp_get_random_related_trips', (user_id, trip_id, 2))
    related_trips = cursor.fetchall()
    cursor.nextset()


    cursor.close()
    conn.close()

    trip_start_date = trip['StartDate']
    trip_end_date = trip['EndDate']
    days = generate_days(trip_start_date, trip_end_date)

    schedule_by_day = {day: [] for day in days}

    for activity in activities:
        if activity['StartDate'] and activity['StartDate'] in schedule_by_day:
            schedule_by_day[activity['StartDate']].append({
                'type': 'Activity',
                'name': activity['ActivityName'],
                'description': activity.get('ActivityDescription', ''),
                'id': activity['ActivityID']
            })

    for accommodation in accommodations:
        if accommodation['CheckInDate'] and accommodation['CheckInDate'] in schedule_by_day:
            schedule_by_day[accommodation['CheckInDate']].append({
                'type': 'Accommodation',
                'name': accommodation['HotelName'],
                'description': 'Hotel Stay',
                'id': accommodation['AccommodationID']
            })

    for transportation in transportations:
        if transportation['StartDate'] and transportation['StartDate'] in schedule_by_day:
            schedule_by_day[transportation['StartDate']].append({
                'type': 'Transportation',
                'name': f"{transportation['StartingPoint']} → {transportation['EndingPoint']}",
                'description': transportation.get('TransportationType', ''),
                'id': transportation['TransportationID']
            })
    
    # Add this to preprocess unscheduled items
    unscheduled_activities = [
        {
            'type': 'Activity',
            'id': activity['ActivityID'],
            'name': activity['ActivityName'],
            'description': activity.get('ActivityDescription', '')
        }
        for activity in unscheduled_activities
    ]

    unscheduled_accommodations = [
        {
            'type': 'Accommodation',
            'id': accommodation['AccommodationID'],
            'name': accommodation['HotelName'],
            'description': 'Hotel Stay'
        }
        for accommodation in unscheduled_accommodations
    ]

    unscheduled_transportations = [
        {
            'type': 'Transportation',
            'id': transportation['TransportationID'],
            'name': f"{transportation['StartingPoint']} → {transportation['EndingPoint']}",
            'description': transportation.get('TransportationType', '')
        }
        for transportation in unscheduled_transportations
    ]


    return render_template('dashboard/trip_detail.html',
                            trip=trip,
                            is_owner=is_owner,
                            activities=activities,
                            accommodations=accommodations,
                            transportations=transportations,
                            unscheduled_activities=unscheduled_activities,
                            unscheduled_accommodations=unscheduled_accommodations,
                            unscheduled_transportations=unscheduled_transportations,
                            total_expense=total_expense,
                            reviews=reviews,
                            days=days,
                            schedule_by_day=schedule_by_day,
                            related_trips=related_trips)

@trips_bp.route('/<int:trip_id>/mark_completed', methods=['POST'])
def mark_trip_as_completed(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Trip.TripID, Trip.UserID, Booking.StatusID,
                   CurrentStatus.IsPending, CurrentStatus.IsCanceled, CurrentStatus.IsConfirmed
            FROM Trip
            LEFT JOIN Booking ON Trip.TripID = Booking.TripID
            LEFT JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
            WHERE Trip.TripID = %s
        """, (trip_id,))
        trip = cursor.fetchone()

        if not trip or trip['UserID'] != user_id:
            flash('You are not authorized to modify this Trip.', 'danger')
            return redirect(url_for('trips.trips_home'))

        if trip['IsConfirmed']:
            flash('Cannot modify a confirmed Trip.', 'danger')
            return redirect(url_for('trips.trip_detail', trip_id=trip_id))

        if trip['IsPending']:
            cursor.execute("""
                SELECT StatusID FROM CurrentStatus WHERE IsCanceled = 1 LIMIT 1
            """)
        else:
            cursor.execute("""
                SELECT StatusID FROM CurrentStatus WHERE IsPending = 1 LIMIT 1
            """)

        new_status = cursor.fetchone()
        if not new_status:
            flash('Target Status not found.', 'danger')
            return redirect(url_for('trips.trip_detail', trip_id=trip_id))

        cursor.execute("""
            UPDATE Booking
            SET StatusID = %s
            WHERE TripID = %s
        """, (new_status['StatusID'], trip_id))

        conn.commit()
        flash('Trip status updated successfully!', 'success')
        return redirect(url_for('trips.trip_detail', trip_id=trip_id))

    except Exception as e:
        conn.rollback()
        flash('An error occurred while updating the Trip status.', 'danger')
        raise e
    finally:
        cursor.close()
        conn.close()


# Trip Publish
@trips_bp.route('/<int:trip_id>/publish', methods=['POST'])
def publish_trip(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Trip.TripID, Trip.UserID, Booking.StatusID
            FROM Trip
            LEFT JOIN Booking ON Trip.TripID = Booking.TripID
            WHERE Trip.TripID = %s
        """, (trip_id,))
        trip = cursor.fetchone()

        if not trip or trip['UserID'] != user_id:
            flash('You are not authorized to publish this Trip.', 'danger')
            return redirect(url_for('trips.trips_home'))

        cursor.execute("""
            SELECT StatusID FROM CurrentStatus WHERE IsConfirmed = 1 LIMIT 1
        """)
        confirmed_status = cursor.fetchone()
        if not confirmed_status:
            flash('Confirmed Status not found.', 'danger')
            return redirect(url_for('trips.trips_home'))

        cursor.execute("""
            UPDATE Booking
            SET StatusID = %s
            WHERE TripID = %s
        """, (confirmed_status['StatusID'], trip_id))

        conn.commit()
        flash('Trip published successfully!', 'success')
        return redirect(url_for('trips.trip_detail', trip_id=trip_id))

    except Exception as e:
        conn.rollback()
        flash('An error occurred while publishing the Trip.', 'danger')
        raise e
    finally:
        cursor.close()
        conn.close()


# Review Trip
@trips_bp.route('/<int:trip_id>/post_review', methods=['POST'])
def post_review(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    review_content = request.form.get('review_content')
    if not review_content:
        flash('Review content cannot be empty.', 'danger')
        return redirect(url_for('trips.trip_detail', trip_id=trip_id))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Review (UserID, TripID, Comments)
            VALUES (%s, %s, %s)
        """, (user_id, trip_id, review_content))

        conn.commit()
        flash('Review posted successfully!', 'success')
        return redirect(url_for('trips.trip_detail', trip_id=trip_id))

    except Exception as e:
        conn.rollback()
        flash('An error occurred while posting review.', 'danger')
        raise e
    finally:
        cursor.close()
        conn.close()


# Editing Trip
@trips_bp.route('/<int:trip_id>/edit', methods=['GET', 'POST'])
def edit_trip(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        new_name = request.form.get('trip_name')
        new_start_date = request.form.get('start_date')
        new_end_date = request.form.get('end_date')
        new_guide_id = request.form.get('guide_id') or None

        try:
            cursor.execute("""
                UPDATE Trip
                SET TripName = %s, StartDate = %s, EndDate = %s, GuideID = %s
                WHERE TripID = %s AND UserID = %s
            """, (new_name, new_start_date, new_end_date, new_guide_id, trip_id, user_id))
            conn.commit()
            flash('Trip updated successfully!', 'success')
            return redirect(url_for('trips.trip_detail', trip_id=trip_id))
        except Exception as e:
            conn.rollback()
            flash('Failed to update trip.', 'danger')
            raise e
        finally:
            cursor.close()
            conn.close()

    else:
        cursor.execute("SELECT * FROM Trip WHERE TripID = %s AND UserID = %s", (trip_id, user_id))
        trip = cursor.fetchone()

        cursor.execute("SELECT GuideID, GuideName FROM Guide")
        guides = cursor.fetchall()

        cursor.close()
        conn.close()

        if not trip:
            flash('Trip not found or you do not have permission.', 'danger')
            return redirect(url_for('trips.trips_home'))

        return render_template('dashboard/edit_trip.html', trip=trip, guides=guides)


# Trip Add Schedule Form
@trips_bp.route('/<int:trip_id>/add_schedule', methods=['POST'])
def add_schedule(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    name = request.form.get('name')
    type_ = request.form.get('type')
    start_date = request.form.get('start_date') or None
    expense = request.form.get('expense') or None
    description = request.form.get('description') or 'N/A'

    if not name or not type_:
        flash('Name and Type are required.', 'danger')
        return redirect(url_for('trips.trip_detail', trip_id=trip_id))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Check if current user can edit this trip
        cursor.execute("""
            SELECT Trip.UserID, CurrentStatus.IsCanceled
            FROM Trip
            LEFT JOIN Booking ON Trip.TripID = Booking.TripID
            LEFT JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
            WHERE Trip.TripID = %s
        """, (trip_id,))
        trip_info = cursor.fetchone()

        if not trip_info or trip_info['UserID'] != user_id or not trip_info['IsCanceled']:
            flash('You are not authorized to modify this Trip.', 'danger')
            return redirect(url_for('trips.trips_home'))

        # Insert based on type
        if type_ == 'Activity':
            # Create a new Activity
            cursor.execute("""
                INSERT INTO Activity (TripID, ActivityName, ActivityDescription, StartDate, Duration)
                VALUES (%s, %s, %s, %s, NULL)
            """, (trip_id, name, description, start_date))
            activity_id = cursor.lastrowid

            if expense:
                cursor.execute("""
                    SELECT TotalExpenseID FROM TotalExpense WHERE TripID = %s
                """, (trip_id,))
                total_expense = cursor.fetchone()
                if total_expense:
                    cursor.execute("""
                        INSERT INTO ActivityExpense (ActivityID, TotalExpenseID, Amount, ExpenseDescription)
                        VALUES (%s, %s, %s, %s)
                    """, (activity_id, total_expense['TotalExpenseID'], expense, 'Activity Expense'))

        elif type_ == 'Accommodation':
            cursor.execute("""
                INSERT INTO Hotel (HotelName, HotelAddress, RoomDescription)
                VALUES (%s, %s, %s)
            """, (name, 'N/A', description))
            hotel_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO Accommodation (TripID, HotelID, CheckInDate, CheckOutDate)
                VALUES (%s, %s, %s, NULL)
            """, (trip_id, hotel_id, start_date))
            accommodation_id = cursor.lastrowid

            if expense:
                cursor.execute("""
                    SELECT TotalExpenseID FROM TotalExpense WHERE TripID = %s
                """, (trip_id,))
                total_expense = cursor.fetchone()
                if total_expense:
                    cursor.execute("""
                        INSERT INTO AccommodationExpense (AccommodationID, TotalExpenseID, Amount, ExpenseDescription)
                        VALUES (%s, %s, %s, %s)
                    """, (accommodation_id, total_expense['TotalExpenseID'], expense, 'Accommodation Expense'))

        elif type_ == 'Transportation':
            cursor.execute("""
                INSERT INTO Transportation (TripID, StartDate, Duration, StartingPoint, EndingPoint, TransportationType)
                VALUES (%s, %s, NULL, %s, %s, %s)
            """, (trip_id, start_date, description, 'Unknown', name))
            transportation_id = cursor.lastrowid

            if expense:
                cursor.execute("""
                    SELECT TotalExpenseID FROM TotalExpense WHERE TripID = %s
                """, (trip_id,))
                total_expense = cursor.fetchone()
                if total_expense:
                    cursor.execute("""
                        INSERT INTO TransportationExpense (TransportationID, TotalExpenseID, Amount, ExpenseDescription)
                        VALUES (%s, %s, %s, %s)
                    """, (transportation_id, total_expense['TotalExpenseID'], expense, 'Transportation Expense'))

        else:
            flash('Invalid type.', 'danger')
            return redirect(url_for('trips.trip_detail', trip_id=trip_id))

        conn.commit()
        flash('Schedule added successfully!', 'success')
        return redirect(url_for('trips.trip_detail', trip_id=trip_id))

    except Exception as e:
        conn.rollback()
        flash('An error occurred while adding schedule.', 'danger')
        raise e
    finally:
        cursor.close()
        conn.close()

# link for modifying trip
@trips_bp.route('/<int:trip_id>/get_item_detail')
def get_item_detail(trip_id):
    item_type = request.args.get('type')
    item_id = request.args.get('id')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if item_type == 'Activity':
            cursor.execute("SELECT ActivityName AS name, ActivityDescription AS description, StartDate AS start_date FROM Activity WHERE ActivityID = %s", (item_id,))
        elif item_type == 'Accommodation':
            cursor.execute("SELECT Hotel.HotelName AS name, Hotel.RoomDescription AS description, Accommodation.CheckInDate AS start_date FROM Accommodation JOIN Hotel ON Accommodation.HotelID = Hotel.HotelID WHERE Accommodation.AccommodationID = %s", (item_id,))
        elif item_type == 'Transportation':
            cursor.execute("SELECT TransportationType AS name, StartingPoint AS description, StartDate AS start_date FROM Transportation WHERE TransportationID = %s", (item_id,))
        else:
            return {'error': 'Invalid type'}, 400

        item = cursor.fetchone()
        if item:
            return jsonify(item)
        else:
            # return {'error': 'Item not found'}, 404
            return jsonify({'error': 'Item not found'}), 404
    finally:
        cursor.close()
        conn.close()

@trips_bp.route('/<int:trip_id>/update_item/<string:item_type>/<int:item_id>', methods=['POST'])
def update_item(trip_id, item_type, item_id):
    user_id = session.get('user_id')
    if not user_id:
        return {'error': 'Unauthorized'}, 401

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    start_date = data.get('start_date') or None

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if item_type == 'Activity':
            cursor.execute("""
                UPDATE Activity
                SET ActivityName = %s, ActivityDescription = %s, StartDate = %s
                WHERE ActivityID = %s
            """, (name, description, start_date, item_id))

        elif item_type == 'Accommodation':
            cursor.execute("""
                UPDATE Hotel
                SET HotelName = %s, RoomDescription = %s
                WHERE HotelID = (
                    SELECT HotelID FROM Accommodation WHERE AccommodationID = %s
                )
            """, (name, description, item_id))
            cursor.execute("""
                UPDATE Accommodation
                SET CheckInDate = %s
                WHERE AccommodationID = %s
            """, (start_date, item_id))

        elif item_type == 'Transportation':
            cursor.execute("""
                UPDATE Transportation
                SET TransportationType = %s, StartingPoint = %s, StartDate = %s
                WHERE TransportationID = %s
            """, (name, description, start_date, item_id))

        else:
            return {'error': 'Invalid type'}, 400

        conn.commit()
        return {'success': True}
    
    except Exception as e:
        conn.rollback()
        print(e)
        return {'error': 'Database error'}, 500
    finally:
        cursor.close()
        conn.close()

# Trip Delete
@trips_bp.route('/<int:trip_id>/delete', methods=['POST'])
def delete_trip(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT UserID FROM Trip WHERE TripID = %s", (trip_id,))
        trip = cursor.fetchone()

        if not trip or trip['UserID'] != user_id:
            flash('You are not authorized to delete this Trip.', 'danger')
            return redirect(url_for('trips.trips_home'))

        cursor.callproc('DeleteTripAndRelatedData', (trip_id,))

        conn.commit()
        flash('Trip deleted successfully!', 'success')
        return redirect(url_for('trips.trips_home'))
    
    except Exception as e:
        conn.rollback()
        flash('An error occurred while deleting the Trip.', 'danger')
        raise e
    finally:
        cursor.close()
        conn.close()


# Destination Homepage
@destination_bp.route('/', methods=['GET'])
def destination_home():
    search_query = request.args.get('search', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("CALL sp_get_destination_by_name(%s)", (search_query,))
    destinations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/destination.html', destinations=destinations, search_query=search_query)

# Destination Detail Page
@destination_bp.route('/<int:destination_id>', methods=['GET'])
def destination_detail(destination_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Destination WHERE DestinationID = %s", (destination_id,))
    destination = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('dashboard/destination_detail.html', destination=destination)

# Tour Guide Homepage
@tour_guide_bp.route('/', methods=['GET'])
def tour_guide_home():
    search_query = request.args.get('search', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("CALL sp_get_guide_by_name(%s)", (search_query,))
    guides = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/tour_guide.html', guides=guides, search_query=search_query)

# Tour Guide Detail Page
@tour_guide_bp.route('/<int:guide_id>', methods=['GET'])
def tour_guide_detail(guide_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Guide WHERE GuideID = %s", (guide_id,))
    guide = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('dashboard/tour_guide_detail.html', guide=guide)

# Hotel Homepage
@hotel_bp.route('/', methods=['GET'])
def hotel_home():
    search_query = request.args.get('search', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("CALL sp_get_hotel_by_name(%s)", (search_query,))
    hotels = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/hotel.html', hotels=hotels, search_query=search_query)

# Hotel Detail Page
@hotel_bp.route('/<int:hotel_id>', methods=['GET'])
def hotel_detail(hotel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Hotel WHERE HotelID = %s", (hotel_id,))
    hotel = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('dashboard/hotel_detail.html', hotel=hotel)

# Transportation New Form
@trips_bp.route('/<int:trip_id>/add_transportation', methods=['GET'])
def add_transportation_form(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Trip.TripID, Trip.UserID, CurrentStatus.IsCanceled
        FROM Trip
        LEFT JOIN Booking ON Trip.TripID = Booking.TripID
        LEFT JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
        WHERE Trip.TripID = %s
    """, (trip_id,))
    trip = cursor.fetchone()

    cursor.close()
    conn.close()

    if not trip:
        flash('Trip not found.', 'danger')
        return redirect(url_for('trips.trips_home'))

    if trip['UserID'] != user_id:
        flash('You are not authorized to modify this Trip.', 'danger')
        return redirect(url_for('trips.trips_home'))

    if not trip['IsCanceled']:
        flash('Only Trips in Public-Cancelled status can be edited.', 'danger')
        return redirect(url_for('trips.trips_home'))

    return render_template('dashboard/add_transportation.html', trip_id=trip_id)


# Add Transportation
@trips_bp.route('/<int:trip_id>/add_transportation', methods=['POST'])
def add_transportation(trip_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    starting_point = request.form.get('starting_point')
    ending_point = request.form.get('ending_point')
    start_date = request.form.get('start_date') or None
    duration = request.form.get('duration') or None
    transportation_type = request.form.get('transportation_type')

    if not starting_point or not ending_point or not transportation_type:
        flash('Starting Point, Ending Point and Transportation Type are required.', 'danger')
        return redirect(url_for('trips.add_transportation_form', trip_id=trip_id))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Trip.TripID, Trip.UserID, CurrentStatus.IsCanceled
            FROM Trip
            LEFT JOIN Booking ON Trip.TripID = Booking.TripID
            LEFT JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
            WHERE Trip.TripID = %s
        """, (trip_id,))
        trip = cursor.fetchone()

        if not trip or trip['UserID'] != user_id or not trip['IsCanceled']:
            conn.rollback()
            flash('You are not authorized to modify this Trip.', 'danger')
            return redirect(url_for('trips.trips_home'))

        cursor.execute("""
            INSERT INTO Transportation (TripID, StartDate, Duration, StartingPoint, EndingPoint, TransportationType)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            trip_id,
            start_date,
            duration,
            starting_point,
            ending_point,
            transportation_type
        ))

        conn.commit()
        flash('Transportation added successfully!', 'success')
        return redirect(url_for('trips.trip_detail', trip_id=trip_id))

    except Exception as e:
        conn.rollback()
        flash('An error occurred. Please try again.', 'danger')
        raise e
    finally:
        cursor.close()
        conn.close()

