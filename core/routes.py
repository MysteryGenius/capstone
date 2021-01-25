from core import app, db
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS, cross_origin
import os
from twilio.rest import Client

account_sid = 'AC13cbd0428b9f0dd27bda86f23863f9b1'
auth_token = 'de6787d9a7ff90c3b8ead763b44e676e'
client = Client(account_sid, auth_token)


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

##### User #####

# Get all user

@app.route('/users/all')
@cross_origin()
def users():
	users = User.query.all()
	result = users_schema.dump(users)
	return jsonify(result)

# Get all user

@app.route('/users/all/users')
@cross_origin()
def users_users():
    users = User.query.filter_by(role='user').all()
    result = users_schema.dump(users)
    return jsonify(result)

# Get a single user or delete user using user_id    

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

# Create a single user

@app.route('/users/add',  methods=['POST'])
@cross_origin()
def new_user():
    if request.is_json:
        email = request.json['email']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        password = request.json['password']
        document_type = request.json['document_type']
        pid = request.json['pid']
        mobile_number = request.json['mobile_number']
        photo = request.json['photo']
        residence_code = request.json['residence_code']
        phone_area_code = request.json['phone_area_code']
        enrolled_id = request.json['enrolled_id']
        organisation_id = request.json['organisation_id']
    else:
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        document_type = request.form['document_type']
        pid = request.form['pid']
        mobile_number = request.form['mobile_number']
        photo = request.form['photo']
        residence_code = request.form['residence_code']
        phone_area_code = request.form['phone_area_code']
        enrolled_id = request.form['enrolled_id']
        organisation_id = request.form['organisation_id']

    commit_new_user = User(
        email=email, password=password, first_name=first_name, last_name=last_name, username=username, document_type=document_type, 
        pid=pid, mobile_number=mobile_number, photo=photo, residence_code=residence_code, phone_area_code=phone_area_code, 
        enrolled_id=enrolled_id, organisation_id=organisation_id
    )
    db.session.add(commit_new_user)
    db.session.commit()
    return jsonify(message="User created!"), 200

@app.route('/user/phone_area_code',  methods=['POST'])
@cross_origin()
def new_user_phone():
    if request.is_json:
        id = request.json['id']
        new_number = request.json['new_number']
    else:
        id = request.form['id']
        new_number = request.json['new_number']

    user = User.query.filter_by(id=id).first()
    user.mobile_number = new_number
    db.session.commit()
    return jsonify(message="User created!"), 200

@app.route('/user/password',  methods=['POST'])
@cross_origin()
def new_user_password():
    if request.is_json:
        id = request.json['id']
        password = request.json['password']
    else:
        id = request.form['id']
        password = request.json['password']

    user = User.query.filter_by(id=id).first()
    user.set_password(password)
    db.session.commit()
    return jsonify(message="User created!"), 200

##### Operators #####

# Get all operators

@app.route('/operators/all')
@cross_origin()
def operators():
    operators = Operator.query.all()
    result = operators_schema.dump(operators)
    return jsonify(result)

# Get a single operator or delete operator using user_id   

@app.route('/operators/<operator_id>',  methods=['GET', 'DELETE'])
@cross_origin()
def get_operator(operator_id):
    if request.method == 'GET':
        operator = Operator.query.filter_by(id=operator_id).first()
        result = operator_schema.dump(operator)
        return jsonify(result)
    if request.method == 'DELETE':
        operator = Operator.query.filter_by(id=operator_id).delete()
        db.session.commit()
        return 200

# Create a single operator

@app.route('/operators/add',  methods=['POST'])
@cross_origin()
def new_operator():
    if request.is_json:
        email = request.json['email']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        password = request.json['password']
        document_type = request.json['document_type']
        pid = request.json['pid']
        mobile_number = request.json['mobile_number']
        photo = request.json['photo']
        residence_code = request.json['residence_code']
        phone_area_code = request.json['phone_area_code']
        enrolled_id = request.json['enrolled_id']
        organisation_id = request.json['organisation_id']
    else:
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        document_type = request.form['document_type']
        pid = request.form['pid']
        mobile_number = request.form['mobile_number']
        photo = request.form['photo']
        residence_code = request.form['residence_code']
        phone_area_code = request.form['phone_area_code']
        enrolled_id = request.form['enrolled_id']
        organisation_id = request.form['organisation_id']

    commit_new_operator = Operator(
        email=email, password=password, first_name=first_name, last_name=last_name, username=username, document_type=document_type, 
        pid=pid, mobile_number=mobile_number, photo=photo, residence_code=residence_code, phone_area_code=phone_area_code, 
        enrolled_id=enrolled_id, organisation_id=organisation_id
    )
    db.session.add(commit_new_operator)
    db.session.commit()
    return jsonify(message="Operator created!"), 200

##### Organization #####

# Get all organizations

@app.route('/organizations/all')
@cross_origin()
def organizations():
    organizations = Organization.query.all()
    result = organizations_schema.dump(organizations)
    return jsonify(result)
        
@app.route('/organizations/<organization_id>',  methods=['GET', 'DELETE'])
@cross_origin()
def get_organization(organization_id):
    if request.method == 'GET':
        organization = Organization.query.filter_by(id=organization_id).first()
        result = organization_schema.dump(organization)
        return jsonify(result)
    if request.method == 'DELETE':
        organization = Organization.query.filter_by(id=organization_id).delete()
        db.session.commit()
        return 200

@app.route('/organizations/add',  methods=['POST'])
@cross_origin()
def new_organization():
    if request.is_json:
        name = request.json['name']
        slug = request.json['slug']
        created_by = request.json['created_by']
    else:
        name = request.form['name']
        slug = request.form['slug']
        created_by = request.form['created_by']

    commit_new_organization = Organization(name=name, slug=slug, created_by=created_by)
    db.session.add(commit_new_organization)
    db.session.commit()
    return jsonify(message="Organization created!"), 200

##### feature #####

# Get all features

@app.route('/features/all')
@cross_origin()
def features():
    features = FacialFeatures.query.all()
    result = facialFeatures_schema.dump(features)
    return jsonify(result)
    
@app.route('/features/<feature_id>',  methods=['GET', 'DELETE'])
@cross_origin()
def get_feature(feature_id):
    if request.method == 'GET':
        feature = FacialFeatures.query.filter_by(id=feature_id).first()
        result = facialFeature_schema.dump(feature)
        return jsonify(result)
    if request.method == 'DELETE':
        feature = FacialFeatures.query.filter_by(id=feature_id).delete()
        db.session.commit()
        return 200

@app.route('/features/add',  methods=['POST'])
@cross_origin()
def new_feature():
    if request.is_json:
        user_id = request.json['user_id']
        face_vector = request.json['face_vector']
    else:
        user_id = request.form['user_id']
        face_vector = request.form['face_vector']

    commit_new_feature = feature(user_id=user_id, face_vector=face_vector)
    db.session.add(commit_new_feature)
    db.session.commit()
    return jsonify(message="FacialFeature created!"), 200


##### Auth Stuff #####

@app.route('/auth/sms/start',  methods=['POST'])
@cross_origin()
def sms_challenge():
    if request.is_json:
        mobile_number = request.json['mobile_number']
    else:
        mobile_number = request.form['mobile_number']

    verification = client.verify \
                     .services('VA20d99c0da1ca85b123ef6c6dd1325875') \
                     .verifications \
                     .create(to=mobile_number, channel='sms')
    return jsonify(message="Challenge created!"), 200

@app.route('/auth/sms/verify',  methods=['POST'])
@cross_origin()
def sms_verify():
    if request.is_json:
        mobile_number = request.json['mobile_number']
        code = request.json['code']
    else:
        mobile_number = request.form['mobile_number']
        code = request.form['code']

    verification_check = client.verify \
                     .services('VA20d99c0da1ca85b123ef6c6dd1325875') \
                     .verification_checks \
                     .create(to=mobile_number, code=code)

    return jsonify(message="Challege Verified : " + verification_check.status), 200


@app.route('/session/<user_id>')
@cross_origin()
def userSessions():
    sessions = UsageHistory.query.filter_by(user_id=user_id).all()
    result = usageHistories_schema.dump(sessions)
    return jsonify(result)

@app.route('/session/users')
@cross_origin()
def userUsersSessions():
    users = User.query.filter_by(role='user').all()
    sessions = UsageHistory.query.filter_by(user_id=users.id).all()
    result = usageHistories_schema.dump(sessions)
    return jsonify(result)


@app.route('/session')
@cross_origin()
def sessions():
    sessions = Session.query.all()
    result = sessions_schema.dump(sessions)
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
        commit_new_session = UsageHistory(user_id=user_id)
        db.session.add(commit_new_session)
        db.session.commit()
        return jsonify(message="Login succeeded!", access_token=access_token) 

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
    curr_user = User.query.filter_by(email=current_user).first()
    return jsonify(user=curr_user.id), 200
