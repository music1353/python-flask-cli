from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

POSTGRES_INFO = {
    'user': 'jensonsu',
    'password': 'bug898beet201',
    'db': 'flasktest',
    'host': 'localhost',
    'port': '5432',
}

postgresql_uri = 'postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'.format(
    dbuser=POSTGRES_INFO['user'],
    dbpass=POSTGRES_INFO['password'],
    dbhost=POSTGRES_INFO['host'],
    dbport=POSTGRES_INFO['port'],
    dbname=POSTGRES_INFO['db']
)