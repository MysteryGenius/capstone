import os
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY = 'dev', # change in production
    JWT_SECRET_KEY = 'super-secret',
    # SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://Test:ToorToor2020@Test',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'core.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import routes
from core.db import *