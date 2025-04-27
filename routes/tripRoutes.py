from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app import get_db_connection

trip_bp = Blueprint('trip', __name__, url_prefix='/trip')

@trip_bp.route('/<int:trip_id>')
def trip_detail(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch trip info
    cursor.execute("SELECT * FROM Trip WHERE TripID = %s", (trip_id,))
    trip = cursor.fetchone()

    cursor.execute("SELECT * FROM TotalExpense WHERE TripID = %s", (trip_id,))
    total_expense = cursor.fetchone()

    conn.close()

    return render_template('trip_detail.html', trip=trip, total_expense=total_expense)

@trip_bp.route('/<int:trip_id>/schedule_list')
def schedule_list(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Schedule WHERE TripID = %s AND Time IS NOT NULL", (trip_id,))
    schedules = cursor.fetchall()

    conn.close()
    return jsonify(schedules)

@trip_bp.route('/<int:trip_id>/unscheduled_list')
def unscheduled_list(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Schedule WHERE TripID = %s AND Time IS NULL", (trip_id,))
    unscheduled = cursor.fetchall()

    conn.close()
    return jsonify(unscheduled)

@trip_bp.route('/<int:trip_id>/add_schedule', methods=['POST'])
def add_schedule(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    name = request.form['name']
    type_ = request.form['type']
    time = request.form.get('time')
    expense = request.form.get('expense', 0)
    description = request.form.get('description')

    cursor.execute("""
        INSERT INTO Schedule (TripID, Name, Type, Time, Expense, Description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (trip_id, name, type_, time if time else None, expense, description))

    conn.commit()
    conn.close()
    return jsonify({'success': True})

@trip_bp.route('/<int:trip_id>/update_schedule/<int:schedule_id>', methods=['POST'])
def update_schedule(trip_id, schedule_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    name = request.form['name']
    type_ = request.form['type']
    time = request.form.get('time')
    expense = request.form.get('expense', 0)
    description = request.form.get('description')

    cursor.execute("""
        UPDATE Schedule
        SET Name = %s, Type = %s, Time = %s, Expense = %s, Description = %s
        WHERE ScheduleID = %s AND TripID = %s
    """, (name, type_, time if time else None, expense, description, schedule_id, trip_id))

    conn.commit()
    conn.close()
    return jsonify({'success': True})

@trip_bp.route('/<int:trip_id>/mark_complete', methods=['POST'])
def mark_complete(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE Trip SET Status = 'Completed' WHERE TripID = %s", (trip_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@trip_bp.route('/<int:trip_id>/publish', methods=['POST'])
def publish(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE Trip SET Status = 'Published' WHERE TripID = %s", (trip_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@trip_bp.route('/get_schedule_detail/<int:schedule_id>')
def get_schedule_detail(schedule_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Schedule WHERE ScheduleID = %s", (schedule_id,))
    schedule = cursor.fetchone()

    conn.close()
    return jsonify(schedule)
