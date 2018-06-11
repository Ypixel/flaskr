from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import Config
from elasticsearch import Elasticsearch

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)
	db.init_app(app)
	migrate.init_app(app,db)
	login.init_app(app)
	bootstrap.init_app(app)

	app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL']  else None


	from blogapp.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from blogapp.auth import bp as auth_bp
	app.register_blueprint(auth_bp,url_prefix='/auth')

	from blogapp.main import bp as main_bp
	app.register_blueprint(main_bp)

	return app

from blogapp import models







