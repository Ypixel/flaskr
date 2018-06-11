import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	
	SECRET_KEY = b'\xd9\x82\xfd\xb7L\x9ey\xe1\x8c\n\xeaNq3.\xfb'
	
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	BOOTSTRAP_SERVE_LOCAL = False

	POST_PER_PAGE = 5

	ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'