# DatabaseFinal
This is a database project using MySQL and Python with Flask.

## Getting Started
The project is a web application, if you want to run it locally, you need to have Python and MySQL installed on your machine. More dependencies are listed in the requirements.txt file. Please make sure to install them.

### Environment Setup
You should have Python 3.x and MySQL installed on your machine. You can use a virtual environment to manage dependencies using `venv` or `pipenv`. Moreover, you need an `.env` file to store your environment variables. You can copy the `.env.example` file and fill in the required values. You should install all the dependencies listed in the `requirements.txt` file in your chosen environment, regardless of whether you are using `venv` or `pipenv`.

### Deploying the Application
- Our database is hosted on [Railway](https://railway.com/) for shared cloud mysql and the current `.env` file is set up to connect to the Railway database. You can change the connection string in the `.env` file to connect to your local MySQL database if you prefer.
- Our app is hosted on localhost, and port 5000 is used by default. You can change the port in the `app.py` file if you want to use a different port.
- After setting up the environment and installing the dependencies, you are suggested to run the following command to create the database and tables:
```bash
python src/initializeDB/initDB.py
python src/indexing/indexing.py
python src/funcAndProc/funcAndProc.py
python src/trigger/trigger.py
```
- Make sure currently your DB role is `root`, and then run:
```bash
python src/dbSecurity/dbSecurity.py
```
to create users and grant permissions. You can change the `.env` file or the `config.py` file to set the database role you want to use. 

You can run `python src/dbSecurity/testIdentity.py` to test whether the database role you are using is correct. If you are using the role of `app user`, you are expected to see an error message, but if you are using the role of `root` or `developer`, you are expected to see success messages.

- Finally, you can run the application using the following command:
```bash
python app.py
```

- The application will be available at `http://localhost:5000/` by default.
    

### Setting Up the Initial Database
There is a directory called `src/` that contains the database initialization scripts. The more detailed instructions are in the section below.

## Repository Structure

- `README.md`: This file, providing an overview of the project.
- `Pipfile`: If you are using Pipenv, this file lists the dependencies for the project.

### Backend
- `app.py`: The main Flask application file.
- `config.py`: Configuration file for the Flask application.
    - Please copy `.env.example` to `.env` and fill in the required values if you haven't done so.
- `src/`: Directory containing the source code from previous milestones.
    - `initializeDB/`: Directory for database initialization scripts.
        - `initDB.py`: Script to initialize the database.
        - `initDB.sql`: SQL script to create the database schema.
        - `insertData.sql`: SQL script to insert initial data into the database.
    - `indexing/`: Directory for indexing scripts.
        - `indexing.py`: Script to create indexes on the database tables.
        - `indexing.sql`: SQL script to create indexes.
    - `funcAndProcs/`: Directory for functions and procedures.
        - `funcAndProcs.py`: Script to create [functions and procedures](https://github.com/SuQichen777/DatabaseFinal/blob/main/src/funcAndProc/funcAndProc.sql) in the database. **The Advanced SQL commands we wrote (except the triggers) in the previous milestone are in this file.**
        - `funcAndProcs.sql`: SQL script to create functions and procedures.
    - `other/`: Directory for other scripts.
        - `other.py`: Script for other database operations.
        - `log.sql`: SQL script for logging. It provides manual logging when operating on the backend. But it is not used in the current version of the project.
    - `dbSecurity/`: Directory for database security scripts **in the Database Level**.
        - `dbSecurity.py`: [Script to create users and grant permissions.](https://github.com/SuQichen777/DatabaseFinal/blob/main/src/dbSecurity/dbSecurity.py)
        - `dbSecurity.sql`: [SQL script to create users and grant permissions.](https://github.com/SuQichen777/DatabaseFinal/blob/main/src/dbSecurity/dbSecurity.sql)
        ``` sql
        CREATE USER 'app_user'@'%' IDENTIFIED BY 'STRONG_APP_USER_PWD';
        CREATE USER 'developer'@'%' IDENTIFIED BY 'STRONG_DEV_PWD';

        GRANT SELECT, INSERT, UPDATE, DELETE ON `TripPlannerDB`.* TO 'app_user'@'%';
        GRANT ALL PRIVILEGES ON `TripPlannerDB`.* TO 'developer'@'%';

        FLUSH PRIVILEGES;
        ```
        - `testIdentity.py`: Script to test the identity of the database users. If you are using the role of `app user`, you are expected to see an error message, but if you are using the role of `root` or `developer`, you are expected to see success messages.
        - `testIdentity.sql`: SQL script to test the identity of the database users.
    - `trigger/`: Directory for triggers.
        - `trigger.py`: Script to create triggers in the database.
        - `trigger.sql`: [SQL script](https://github.com/SuQichen777/DatabaseFinal/blob/main/src/trigger/trigger.sql) to create triggers. Also written **in the previous milestone**.
- `routes/`: Directory for Flask routes.
        

### Frontend
- `static/`: Directory for static files (CSS, JavaScript, images).
- `templates/`: Directory for HTML templates.

### Database Security at the Application Level
- When dealing with a form with write operations, we use `try...except` to catch exceptions and display error messages and use `rollback()` to roll back the transaction if an error occurs. For example, this is a [function](https://github.com/SuQichen777/DatabaseFinal/blob/main/routes/dashboardRoutes.py) to post a new review with a form in `dashboardRoutes.py`:
```python
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
```

- We use password hashing to store passwords securely. 
``` python
from werkzeug.security import generate_password_hash, check_password_hash  # for password hashing
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
```
This is our [registration route](https://github.com/SuQichen777/DatabaseFinal/blob/main/app.py) in `app.py`. 