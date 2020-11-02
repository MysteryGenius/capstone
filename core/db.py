from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow


def init_app(app):
	db = SQLAlchemy(app)
	ma = Marshmallow(app)

	@app.cli.command('db_create')
	def db_create():
	    db.create_all()
	    print('Database created!')


	@app.cli.command('db_drop')
	def db_drop():
	    db.drop_all()
	    print('Database dropped!')

	@app.cli.command('db_seed')
	def db_seed():
	    test_user = User(first_name='William',
	                     last_name='Herschel',
	                     email='test@test.com',
	                     password='password')

	    db.session.add(test_user)
	    db.session.commit()
	    print("Database Seeded")

	class User(db.Model):
		__tablename__ = 'users'
		id = Column(Integer, primary_key=True)
		first_name = Column(String)
		last_name = Column(String)
		email = Column(String, unique=True)
		password = Column(String)

	class UserSchema(ma.Schema):
		class Meta:
			fields = ('id', 'first_name', 'last_name', 'email', 'password')

	user_schema = UserSchema()
	users_schema = UserSchema(many=True)
