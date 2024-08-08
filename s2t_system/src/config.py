import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

REDIS_HOST = os.environ.get('REDIS_HOST')

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS')
