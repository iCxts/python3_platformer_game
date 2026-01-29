import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 3000))
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
