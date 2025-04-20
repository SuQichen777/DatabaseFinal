from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Conn
def get_db_connection():
    connection = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        port=config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Home page
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))
    
# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username=%s AND password=%s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                if user:
                    session['username'] = user['username']
                    flash('Logged in successfully!')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid username or password')
        finally:
            connection.close()
    
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('home'))

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # check if the username already exists
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    flash('Username already exists. Please choose another one.')
                    return redirect(url_for('register'))
                
                # insert new user into the database
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, password))
                connection.commit()
                flash('Registration successful! You can now login.')
                return redirect(url_for('login'))
        finally:
            connection.close()
    
    return render_template('register.html')

# 新增一个数据（示例）
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    age = request.form.get('age')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Users (name, age) VALUES (%s, %s)"
            cursor.execute(sql, (name, age))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
