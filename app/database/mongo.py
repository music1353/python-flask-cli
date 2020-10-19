import pymongo

MONGO_INFO = {
    'user': 'admin',
    'password': 'mongoadmin',
    'db': 'horizone',
    'host': '35.234.23.126',
    'port': '27017',
}

mongo_uri = 'mongodb://{dbuser}:{dbpass}@{dbhost}:{dbport}'.format(
    dbuser=MONGO_INFO['user'],
    dbpass=MONGO_INFO['password'],
    dbhost=MONGO_INFO['host'],
    dbport=MONGO_INFO['port']
)


client = pymongo.MongoClient(mongo_uri, connect=False)
db = client['myMongo']

