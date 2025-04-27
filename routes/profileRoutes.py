from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import get_db_connection

profile_bp = Blueprint('profile', __name__)

# profile and settings
@profile_bp.route('/profile')
@profile_bp.route('/profile/settings')
def profile():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.callproc('sp_get_user_by_name', (session['user_name'],))
    user_info = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('profile.html', user=user_info)

# update profile
@profile_bp.route('/profile/update', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        form_token = request.form.get('csrf_token')
        if not form_token or form_token != session.get('csrf_token'):
            flash('Invalid CSRF token. Please try again.')
            return redirect(url_for('profile.update_profile'))
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # fetch user info
        cursor.callproc('sp_get_user_by_name', (session['user_name'],))
        user_info = cursor.fetchone()

        if not user_info:
            flash('User not found.')
            return redirect(url_for('profile.profile'))
        
        name = request.form['name']
        phone = request.form.get('phone', 'N/A')
        email = user_info['Email']  # email is not editable
        age = request.form.get('age', 0)
        preference = request.form.get('preference', 'No preference')

        cursor.callproc('UpdateUserInfo', (session['user_id'], name, phone, email, age, preference))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Profile updated successfully.')
        return redirect(url_for('profile.profile'))

    # GET request
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('sp_get_user_by_name', (session['user_name'],))
    user_info = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('update_profile.html', user=user_info)

# My Trips (trips created by the user)
@profile_bp.route('/profile/my_trips')
def my_trips():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('sp_get_trips_by_user', (session['user_id'],))
    trips = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('my_trips.html', trips=trips)

# My Collections (trips collected by the user)
@profile_bp.route('/profile/my_collections')
def my_collections():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('sp_get_collected_trips_by_user', (session['user_id'],))
    collections = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('my_collections.html', trips=collections)
