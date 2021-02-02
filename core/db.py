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
        role='admin',
        mobile_number='122433545',
		email='wubbalubba@dubdub.com')

    test_user_2 = User(
    	first_name='Jian Zhen',
		last_name='Tan',
        role='user',
        mobile_number='122433545',
		email='jayz@oi.wtf')

    test_user_3 = User(
        first_name='Yue Kai',
        last_name='Tan',
        role='user',
        mobile_number='14543545',
        email='sam@oi.wtf')

    test_user_4 = User(
        first_name='Jian Zhe',
        last_name='Tan',
        role='user',
        mobile_number='455443545',
        email='onella@oi.wtf')

    test_user_5 = User(
        first_name='Jabier',
        last_name='Wubbalubba',
        role='operator',
        mobile_number='1563545',
        email='jabier@oi.wtf')

    test_org_1 = Organization(
        name='Cumpani',
        slug='Cump',
        sttaus='live',
        contact='1563545',
        email='jabier@cumpani.wtf')

    test_org_1 = Organization(
        name='Floridaman',
        slug='Flor',
        sttaus='live',
        contact='1563545',
        email='Sam@floridaman.wtf')

    test_user_1.set_password('password')
    test_user_2.set_password('password')
    test_user_3.set_password('password')
    test_user_4.set_password('password')
    test_user_5.set_password('password')
    db.session.add(test_user_1)
    db.session.add(test_user_2)
    db.session.add(test_user_3)
    db.session.add(test_user_4)
    db.session.add(test_user_5)

    db.session.add(test_org_1)
    db.session.add(test_org_2)
    db.session.commit()
    print("Database Seeded")
