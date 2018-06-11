from flask import Blueprint

bp = Blueprint('main',__name__)

from blogapp.main import routes
