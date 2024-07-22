import os
from dotenv import load_dotenv

load_dotenv('../.env')

TEST = bool(os.environ.get("TEST"))
# SECRET KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'SECRET_KEY')

# DATABASE SETTINGS
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'taqqos_parsing')
DATABASE_USER = os.environ.get('DATABASE_USER', 'taqqos_parsing')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'taqqos_parsing')
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5431')

if TEST:
    DATABASE_URL = "sqlite:///database.db"
else:
    DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'