set FLASK_APP=core
set FLASK_ENV=development
flask db_create
flask db_seed
flask run