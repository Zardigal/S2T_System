from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.environ.get('JWT_SECRET')
