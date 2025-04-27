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
```
- Make sure currently your DB role is `root`, and then run:
```bash
python src/dbSecurity/dbSecurity.py
```
to create users and grant permissions. You can change the `.env` file or the `config.py` file to set the database role you want to use. You can run `src/dbSecurity/testIdentity.py` to test whether the database role you are using is correct. If you are using the role of `app user`, you are expected to see an error message, but if you are using the role of `root` or `developer`, you are expected to see success messages.

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
    - Please copy `.env.example` to `.env` and fill in the required values.
- `src/`: Directory containing the source code from previous milestones.
    - `initializeDB/`: Directory for database initialization scripts.
        - `initDB.py`: Script to initialize the database.
        - `initDB.sql`: SQL script to create the database schema.
        - `insertData.sql`: SQL script to insert initial data into the database.
    - `indexing/`: Directory for indexing scripts.
        - `index.py`: Script to create indexes on the database tables.
        - `index.sql`: SQL script to create indexes.
    - `funcAndProcs/`: Directory for functions and procedures.
        - `funcAndProcs.py`: Script to create functions and procedures in the database. **The Advanced SQL commands we wrote in the previous milestone are in this file.**
        - `funcAndProcs.sql`: SQL script to create functions and procedures.
    - `other/`: Directory for other scripts.
        - `other.py`: Script for other database operations.
        - `log.sql`: SQL script for logging. It provides manual logging when operating on the backend. But it is not used in the current version of the project.
    - `dbSecurity/`: Directory for database security scripts **in the Database Level**.
        - `dbSecurity.py`: Script to create users and grant permissions.
        - `dbSecurity.sql`: SQL script to create users and grant permissions.
        - `testIdentity.py`: Script to test the identity of the database users. If you are using the role of `app user`, you are expected to see an error message, but if you are using the role of `root` or `developer`, you are expected to see success messages.
        - `testIdentity.sql`: SQL script to test the identity of the database users.
    
- `routes/`: Directory for Flask routes.
        

### Frontend
- `static/`: Directory for static files (CSS, JavaScript, images).
- `templates/`: Directory for HTML templates.