from flask import Blueprint, render_template

from .services import *
from library.adapters.repository import repo_instance as repo

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/')  # , methods=['GET'])
def home():
    recent_books = get_recent_books(repo)
    return render_template('home/home.html', books=recent_books)
