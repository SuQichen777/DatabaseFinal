import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

db_url = os.getenv('MYSQL_PUBLIC_URL')
parsed = urlparse(db_url)


class Config:
    DB_HOST = parsed.hostname
    DB_PORT = parsed.port
    DB_USER = parsed.username # root choice
    # DB_USER = os.getenv('DB_USER') # app_user
    DB_PASSWORD = parsed.password # root choice
    # DB_PASSWORD = os.getenv('DB_PASSWORD') # app user password
    DB_NAME = parsed.path.lstrip('/')
