from flask import Blueprint, render_template

from .services import *
from library.adapters.repository import repo_instance as repo

home_blueprint = Blueprint('home_bp', __name__)

recommended_books = [12898900, 2687401, 1348630, 11827783]

@home_blueprint.route('/')  # , methods=['GET'])
def home():
    recent_books = get_recommended_books(repo, recommended_books)
    return render_template('home/home.html', books=recent_books)
