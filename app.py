from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash  # for password hashing
from config import Config

app = Flask(__name__)
import secrets

# Use CSRF Token to prevent CSRF attacks
@app.before_request
def set_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

app.secret_key = os.urandom(24)

# Conn
def get_db_connection():
    connection = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


# Homepage
@app.route('/')
def index():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE UserID = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('index.html', user_data=user_data)


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_token = request.form.get('csrf_token')
        if not form_token or form_token != session.get('csrf_token'):
            flash('Invalid CSRF token. Please try again.')
            return redirect(url_for('register'))
        name = request.form['name']
        password = request.form['password']
        phone = request.form.get('phone', 'N/A')
        email = request.form['email']
        age = request.form.get('age')
        preference = request.form.get('preference', 'No preference')

        # Although we made the fields optional, we still have to check if they are empty
        if not age.isdigit():
            age = 0
        if not preference:
            preference = 'No preference'
        if not phone:
            phone = 'N/A'
        if not name or not password or not email:
            flash('Please fill in all fields.')
            return redirect(url_for('register'))
        conn = get_db_connection()
        cursor = conn.cursor()

        # We restrict the email to be unique
        cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('register'))

        # Insert new user
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO Users (Name, Password, PhoneNumber, Email, Age, Preference) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, hashed_password, phone, email, age, preference)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('You are already logged in.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        form_token = request.form.get('csrf_token')
        if not form_token or form_token != session.get('csrf_token'):
            flash('Invalid CSRF token. Please try again.')
            return redirect(url_for('login'))
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Manually check password for UserID <= 10
            if user['UserID'] <= 10:
                if password == user['Password']:
                    session['user_id'] = user['UserID']
                    session['user_name'] = user['Name']
                    flash('Login successful!')
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect password.')
                    return redirect(url_for('login'))
            else:
                # Hash password for UserID > 10
                if check_password_hash(user['Password'], password):
                    session['user_id'] = user['UserID']
                    session['user_name'] = user['Name']
                    flash('Login successful!')
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect password.')
                    return redirect(url_for('login'))
        else:
            flash('Email not found.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

# @app.route('/profile')
# def profile():
#     return "<h1>Profile page under construction.</h1>"

@app.route('/trip')
def trip():
    return "<h1>Trip page under construction.</h1>"

@app.route('/tourguide')
def tourguide():
    return "<h1>Tour Guide page under construction.</h1>"

@app.route('/hotel')
def hotel():
    return "<h1>Hotel page under construction.</h1>"

@app.route('/destination')
def destination():
    return "<h1>Destination page under construction.</h1>"


# Other routes
try:
    from routes import all_blueprints
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
except ImportError:
    pass

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
