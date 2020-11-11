from core import app, db, ma
from sqlalchemy import Column, Integer, String, Float

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String, unique=True)
	password = Column(String) # bcrypt hashed

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

class UserSchema(ma.Schema):
	class Meta:
		fields = ('id', 'first_name', 'last_name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Session(db.Model):
	__tablename__ = 'sessions'
	id = Column(Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	jwt = Column(String, default='unassigned')
	created_on = db.Column(db.DateTime, server_default=db.func.now())
	updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class SessionSchema(ma.Schema):
	class Meta:
		fields = ('id', 'user_id', 'jwt')

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)