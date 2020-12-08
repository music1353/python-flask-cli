from app.database import db
from app.pkg.err_handler import error


user_collect = db['users']

class User:
    '''User Schema
        uid         {str}
        nickname    {int}
        avatar      {str}
        like_topics {dict-list}
            - forum_id {str}
            - topic_id {str}
    '''
    @classmethod
    def check_nickname(cls, nickname:str) -> str:
        err = None
        exist = cls._check_duplicated_nickname(nickname)
        return exist, err
    

    @classmethod
    def insert_one(cls, uid:str, nickname:str, avatar:str) -> str:
        err = None

        user = {
            'uid': uid,
            'nickname': nickname,
            'avatar': avatar,
            'like_topics': []
        }

        try:
            user_collect.insert_one(user)
        except Exception as e:
            err = error(e)
        
        return err

    
    @staticmethod
    def find_one(uid:str) -> (dict, str):
        data = dict()
        err = None

        user = {
            'uid': uid
        }

        try:
            user_doc = user_collect.find_one(user, {'_id': False})
            if user_doc:
                data = {
                    'uid': user_doc['uid'],
                    'nickname': user_doc['nickname'],
                    'avatar': user_doc['avatar']
                }
        except Exception as e:
            err = error(e)

        return data, err
    

    @staticmethod
    def _check_duplicated_nickname(nickname:str) -> bool:
        flag = False

        doc = user_collect.find_one({'nickname': nickname}, {'_id': False})
        if doc:
            flag = True
        
        return flag
