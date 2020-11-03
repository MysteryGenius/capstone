from core import app
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from core.models import *

@app.route('/')
def index():
    return jsonify('Hallo! You are now connected to the FacePass Backend')

@app.route('/users')
def users():
	users = User.query.all()
	result = users_schema.dump(users)
	return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email).first()

    if test is None or not test.check_password(password):
        return jsonify(message="Bad email or password"), 401
    else:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)