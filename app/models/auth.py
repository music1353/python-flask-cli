import random
from datetime import datetime

from app.database import db
from app.pkg.err_handler import error


auth_collect = db['auths']

class Auth:
    '''Auth Schema
        uid              {str}
        role             {int} 1=user|2=admin
        identity_type    {str} email|google
        identifier       {str}
        credential       {str}
        created_datetime {str}
    '''
    @classmethod
    def check_identifier(cls, identifier:str) -> str:
        err = None
        exist = cls._check_duplicated_identifier(identifier)
        return exist, err


    @classmethod
    def insert_one(cls, identify_type:str, identifier:str, credential:str, check_policy:bool) -> (str, str):
        uid = ''.join(str(i) for i in random.sample(range(0,9), 8))
        err = None

        # check duplicated
        while cls._check_duplicated_uid(uid):
            uid = ''.join(str(i) for i in random.sample(range(0,9), 8))

        # insert auth
        auth = {
            'uid': uid,
            'role': 1,
            'identify_type': identify_type,
            'identifier': identifier,
            'credential': credential,
            'check_policy': check_policy,
            'created_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            auth_collect.insert_one(auth)
        except Exception as err:
            err = error(e)
        
        return uid, err


    @classmethod
    def find_one(cls, identifier:str, credential:str) -> (dict, str):
        data = {}
        err = None

        auth = {
            'identifier': identifier,
            'credential': credential
        }

        try:
            auth_doc = auth_collect.find_one(auth, {'_id': False})
            if auth_doc:
                data = {
                    'uid': auth_doc['uid'],
                    'role': auth_doc['role'],
                    'identifier': auth_doc['identifier']
                }
        except Exception as e:
            err = error(e)
        
        return data, err


    @classmethod
    def _check_duplicated_uid(cls, uid:str) -> bool:
        flag = False

        doc = auth_collect.find_one({'uid': uid}, {'_id': False})
        if doc:
            flag = True
        return flag


    @classmethod
    def _check_duplicated_identifier(cls, identifier:str) -> bool:
        flag = False
        
        try:
            doc = auth_collect.find_one({'identifier': identifier}, {'_id': False})
            if doc:
                flag = True
        except Exception as e:
            err = error(e)
        
        return flag


    