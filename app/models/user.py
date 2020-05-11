from app.database import db
from app.pkg.err_handler import error
from . import SQLSerial

class User(db.Model, SQLSerial):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, db.ForeignKey('auths.id'), primary_key=True)
    name = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)

    db_user_auth_relation = db.relationship("Auth", backref="auths")

    def __init__(self, uid, name, phone):
        self.uid = uid
        self.name = name
        self.phone = phone

    @staticmethod
    def insert_one(uid, name, phone):
        err = str()

        user = User(uid, name, phone)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            err = error(e)
            current_app.logger.error(err)
        
        return err

    
    @staticmethod
    def get_all_users():
        query = User.query.all()

        return SQLSerial.serialize(query)

