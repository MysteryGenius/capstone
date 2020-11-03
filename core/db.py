from flask.cli import with_appcontext

from core import app, db, ma
from core.models import *

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
    test_user_1 = User(
    	first_name='Rick',
		last_name='Sanchez',
		email='wubbalubba@dubdub.com')

    test_user_2 = User(
    	first_name='Jian Zhen',
		last_name='Tan',
		email='jayz@oi.wtf')

    test_user_1.set_password('password')
    test_user_2.set_password('password')
    db.session.add(test_user_1)
    db.session.add(test_user_2)
    db.session.commit()
    print("Database Seeded")
