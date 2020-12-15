from core import app, db
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS, cross_origin


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

from core.models import *

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/user/image/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 200

@app.route('/')
@cross_origin()
def index():
    return jsonify('Hallo! You are now connected to the FacePass Backend')

@app.route('/users/all')
@cross_origin()
def users():
	users = User.query.all()
	result = users_schema.dump(users)
	return jsonify(result)
    
@app.route('/users/<user_id>',  methods=['GET', 'DELETE'])
@cross_origin()
def get_user(user_id):
    if request.method == 'GET':
        user = User.query.filter_by(id=user_id).first()
        result = user_schema.dump(user)
        return jsonify(result)
    if request.method == 'DELETE':
        user = User.query.filter_by(id=user_id).delete()
        db.session.commit()
        return 200

@app.route('/users/add',  methods=['POST'])
@cross_origin()
def new_user():
    if request.is_json:
        email = request.json['email']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        role = request.json['role']
        password = request.json['password']
    else:
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        role = request.form['role']
        password = request.form['password']

    commit_new_user = User(email=email, password=password, first_name=first_name, last_name=last_name, role=role)
    db.session.add(commit_new_user)
    db.session.commit()
    return jsonify(message="User created!"), 200

@app.route('/session')
@cross_origin()
def sessions():
    sessions = Session.query.all()
    result = sessions_schema.dump(sessions)
    return jsonify(result)

@app.route('/login', methods=['POST'])
@cross_origin()
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
        # access_token = create_access_token(identity=email)
        curr_session = Session(user_id=test.id)
        db.session.add(curr_session)
        db.session.commit()
        curr_session = Session.query.filter_by(user_id=test.id).first()
        result = session_schema.dump(curr_session)
        return jsonify(message="Session created!", session=result), 200

@app.route('/face', methods=['POST'])
@cross_origin()
def face():
    if request.is_json:
        session_id = request.json['session_id']
        image = request.json['image']
    else:
        session_id = request.form['session_id']
        image = request.form['image']

    curr_session = Session.query.filter_by(id=session_id).first()
    curr_user = User.query.filter_by(id=curr_session.user_id).first()
    if curr_session:
        access_token = create_access_token(identity=curr_user.email)
        return jsonify(message="Login succeeded!", access_token=access_token), 200
    else:
        return jsonify(message="FacePass failed!"), 400

@app.route('/check', methods=['GET'])
@jwt_required
def check():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(user=current_user), 200