from core import app, db, ma
from sqlalchemy import Column, Integer, String, Float, BigInteger

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String)
	first_name = Column(String)
	last_name = Column(String)
	role = Column(String)
	document_type = Column(String, nullable=True)					# Enum (Passport, NRIC, FIN)
	pid = Column(String)							# Last 4 characters on personal IC
	mobile_number = Column(String)
	country = Column(String)
	photo = Column(String, nullable=True)
	residence_code = Column(String)
	phone_area_code = Column(String)
	password = Column(String)						# bcrypt hashed
	email = Column(String, unique=True)
	status = Column(String, default="active")						# Enum (active, disabled)

	enrolled_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
	organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"), nullable=True)

	created_on = db.Column(db.DateTime, server_default=db.func.now())
	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

class UserSchema(ma.Schema):
	class Meta:
		fields = ('id', 'username', 'first_name', 'last_name', 'country', 'role', 'email', 'status', 'document_type', 'pid', 'mobile_number', 'photo', 'residence_code', 'phone_area_code', 'enrolled_id', 'organisation_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# class Operator(db.Model):
# 	__tablename__ = 'operators'
# 	id = Column(Integer, primary_key=True)
# 	username = Column(String)
# 	first_name = Column(String)
# 	last_name = Column(String)
# 	document_type = Column(String, nullable=True)					# Enum (Passport, NRIC, FIN)
# 	pid = Column(String)							# Last 4 characters on personal IC
# 	mobile_number = Column(String)
# 	photo = Column(String, nullable=True)
# 	residence_code = Column(String)
# 	phone_area_code = Column(String)
# 	password = Column(String)						# bcrypt hashed
# 	email = Column(String, unique=True)
# 	status = Column(String, default="active")						# Enum (active, disabled)
# 	enrolled_id = db.Column(db.Integer, db.ForeignKey('operators.id'), nullable=True)
# 	organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=True)

# 	created_on = db.Column(db.DateTime, server_default=db.func.now())
# 	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

# 	def set_password(self, password):
# 		self.password = generate_password_hash(password)

# 	def check_password(self, password):
# 		return check_password_hash(self.password, password)

# class OperatorSchema(ma.Schema):
# 	class Meta:
# 		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'status', 'document_type', 'pid', 'mobile_number', 'photo', 'residence_code', 'phone_area_code', 'enrolled_id', 'organisation_id')

# operator_schema = OperatorSchema()
# operators_schema = OperatorSchema(many=True)


class Session(db.Model):
	__tablename__ = 'sessions'
	id = Column(Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
	jwt = Column(String, default='unassigned')

	created_on = db.Column(db.DateTime, server_default=db.func.now())
	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class SessionSchema(ma.Schema):
	class Meta:
		fields = ('id', 'user_id', 'jwt')

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

class FacialFeatures(db.Model):
	__tablename__ = 'features'
	id = Column(Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
	face_vector = Column(Float)

	created_on = db.Column(db.DateTime, server_default=db.func.now())
	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class FacialFeatureSchema(ma.Schema):
	class Meta:
		fields = ('id', 'user_id', 'face_vector')

facialFeature_schema = FacialFeatureSchema()
facialFeatures_schema = FacialFeatureSchema(many=True)

class UsageHistory(db.Model):
	__tablename__ = 'usage_history'
	id = Column(Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
	geocode = Column(String)
	history = Column(String)

	created_on = db.Column(db.DateTime, server_default=db.func.now())
	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class UsageHistorySchema(ma.Schema):
	class Meta:
		fields = ('id', 'user_id', 'geocode', 'history')

usageHistory_schema = UsageHistorySchema()
usageHistories_schema = UsageHistorySchema(many=True)

class Organization(db.Model):
	__tablename__ = 'organisations'
	id = Column(Integer, primary_key=True)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
	name = Column(String)
	email = Column(String)
	contact = Column(String)
	slug = Column(String)
	status = Column(String)

	created_on = db.Column(db.DateTime, server_default=db.func.now())
	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class OrganizationSchema(ma.Schema):
	class Meta:
		fields = ('id', 'created_by', 'contact', 'name', 'email', 'slug', 'status')

organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)		