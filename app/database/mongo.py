import pymongo

MONGO_INFO = {
    'user': 'admin',
    'password': 'mongoadmin',
    'db': 'myMongo'
    'host': 'localhost',
    'port': '27017',
}

mongo_uri = 'mongodb://{dbuser}:{dbpass}@{dbhost}:{dbport}'.format(
    dbuser=MONGO_INFO['user'],
    dbpass=MONGO_INFO['password'],
    dbhost=MONGO_INFO['host'],
    dbport=MONGO_INFO['port']
)

try:
    client = pymongo.MongoClient(mongo_uri, connect=False)
    print('Successfully connect to mongodb!')
except Exception as err:
    print('Error: connect to mongodb failed.', err)

db = client[MONGO_INFO['db']]

