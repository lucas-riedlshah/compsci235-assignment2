"""Flask configuration variables."""
from os import environ
from dotenv import load_dotenv

from utils import get_project_root

# Load environment variables from file .env, stored in this directory.
load_dotenv(get_project_root() / '.env')

class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')

    TESTING = environ.get('TESTING')

    REPOSITORY = environ.get('REPOSITORY')

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = True if environ.get('SQLALCHEMY_ECHO').strip().lower() == 'true' else False