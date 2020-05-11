from flask import current_app
from datetime import datetime
from app.database import db
from app.pkg.err_handler import error
from . import SQLSerial

class Auth(db.Model, SQLSerial):
    __tablename__ = 'auths'
    id = db.Column(db.Integer, primary_key=True)
    identify_type = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    credential = db.Column(db.String, nullable=False)
    sign_up_datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, identify_type, identifier, credential):
        self.identify_type = identify_type
        self.identifier = identifier
        self.credential = credential

    @staticmethod
    def insert_one(identify_type:str, identifier:str, credential:str) -> (int, str):
        uid = int()
        err = str()

        auth = Auth(identify_type=identify_type, identifier=identifier, credential=credential)
        try:
            db.session.add(auth)
            db.session.commit()
            db.session.flush()
            uid = auth.id
        except Exception as e:
            err = error(e)
            current_app.logger.error(err)
            
        return uid, err
        
    
    @staticmethod
    def check_auth(identifier:str, credential:str) -> dict:
        ''' 確認是否有此用戶
            Params:
                - identifier {string} user's account
                - credential {string} user's password
            Return:
                - data {dict} (
                    - is_exist {bool}
                    - identifier {string}
                )
        '''
        data = {
            'is_exist': False,
            'identifier': ''
        }

        res = Auth.query.filter_by(identifier=identifier, credential=credential).first()

        if res is not None:
            data['is_exist'] = True
            data['identifier'] = res.identifier
        
        return data
