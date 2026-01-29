import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "dev-key"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

HOST = "0.0.0.0"
PORT = 3000
DEBUG = True
