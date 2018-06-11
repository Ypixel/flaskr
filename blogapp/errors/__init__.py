from flask import Blueprint

bp = Blueprint('errors',__name__)


from blogapp.errors import handlers