from flask import Blueprint, render_template, request
from app import get_db_connection

trips_bp = Blueprint('trips', __name__, url_prefix='/trips')
destination_bp = Blueprint('destination', __name__, url_prefix='/destination')
tour_guide_bp = Blueprint('tour_guide', __name__, url_prefix='/tour_guide')
hotel_bp = Blueprint('hotel', __name__, url_prefix='/hotel')

@trips_bp.route('/', methods=['GET'])
def trips_home():
    search_query = request.args.get('search')
    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:
        cursor.execute("SELECT * FROM Trip WHERE TripName LIKE %s", (f"%{search_query}%",))
        trips = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Trip ORDER BY RAND() LIMIT 3")
        trips = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/trips.html', trips=trips, search_query=search_query)

@trips_bp.route('/<int:trip_id>', methods=['GET'])
def trip_detail(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trip WHERE TripID = %s", (trip_id,))
    trip = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('dashboard/trip_detail.html', trip=trip)

@destination_bp.route('/', methods=['GET'])
def destination_home():
    search_query = request.args.get('search')
    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:
        cursor.execute("SELECT * FROM Destination WHERE City LIKE %s", (f"%{search_query}%",))
        destinations = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Destination ORDER BY RAND() LIMIT 3")
        destinations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/destination.html', destinations=destinations, search_query=search_query)

@destination_bp.route('/<int:destination_id>', methods=['GET'])
def destination_detail(destination_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Destination WHERE DestinationID = %s", (destination_id,))
    destination = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('dashboard/destination_detail.html', destination=destination)

@tour_guide_bp.route('/', methods=['GET'])
def tour_guide_home():
    search_query = request.args.get('search')
    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:
        cursor.execute("SELECT * FROM Guide WHERE GuideName LIKE %s", (f"%{search_query}%",))
        guides = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Guide ORDER BY RAND() LIMIT 3")
        guides = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/tour_guide.html', guides=guides, search_query=search_query)

@tour_guide_bp.route('/<int:guide_id>', methods=['GET'])
def tour_guide_detail(guide_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Guide WHERE GuideID = %s", (guide_id,))
    guide = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('dashboard/tour_guide_detail.html', guide=guide)

@hotel_bp.route('/', methods=['GET'])
def hotel_home():
    search_query = request.args.get('search')
    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:
        cursor.execute("SELECT * FROM Hotel WHERE HotelName LIKE %s", (f"%{search_query}%",))
        hotels = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Hotel ORDER BY RAND() LIMIT 3")
        hotels = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard/hotel.html', hotels=hotels, search_query=search_query)

@hotel_bp.route('/<int:hotel_id>', methods=['GET'])
def hotel_detail(hotel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Hotel WHERE HotelID = %s", (hotel_id,))
    hotel = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('dashboard/hotel_detail.html', hotel=hotel)
