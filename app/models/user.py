from app.database import db
from . import SQLSerial

class User(db.Model, SQLSerial):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)

    def __init__(self, id, name, phone):
        self.id = id
        self.name = name
        self.phone = phone
    
    @staticmethod
    def get_all_users():
        query = User.query.all()

        return SQLSerial.serialize(query)

