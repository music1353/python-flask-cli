class SQLSerial:
    def to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict

    @staticmethod
    def serialize(data):
        res = []
        for d in data:
            res.append(d.to_dict())
        return res


from .role import Role
from .permission import Permission
from .user import User
from .auth import Auth