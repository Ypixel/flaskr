from flask import Blueprint

bp = Blueprint('auth',__name__)


from blogapp.auth import routes