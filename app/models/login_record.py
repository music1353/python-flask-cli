from datetime import datetime

from app.database import db
from app.pkg.err_handler import error


login_record_collect = db['login_records']

class LoginRecord:
    '''LoginRecord Schema
        uid                 {str}
        lastest_login_ip    {str}
        lastest_login_time  {str}
        records             {dict-list}
            - ip       {str}
            - time     {str}
            - isChange {bool}
    '''
    @staticmethod
    def init_one(uid:str) -> str:
        err = None

        login_record = {
            'uid': uid,
            'lastest_login_ip': '',
            'lastest_login_time': '',
            'records': []
        }

        try:
            login_record_collect.insert_one(login_record)
        except Exception as e:
            err = error(e)
        
        return err
    

    @staticmethod
    def update_one(uid:str, ip:str) -> str:
        err = None

        try:
            # 紀錄登入ip
            login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            login_record = {
                'lastest_login_ip': ip,
                'lastest_login_time': login_time
            }
            login_record_collect.update_one({'uid': uid}, {'$set': login_record})
        
            # 是否有不同的ip登入位置
            login_record_doc = login_record_collect.find_one({'uid': uid}, {'_id': False})
            change_flag = False # 判別是否有更改登入位置
            if (len(login_record_doc['records']) > 0): # 有過去的登入資料
                if (login_record_doc['records'][len(login_record_doc['records'])-1]['ip'] != ip):
                    change_flag = True

            login_record = {
                'ip': ip,
                'time': login_time,
                'isChange': change_flag
            }
            login_record_collect.update_one({'uid': uid}, {'$push': {'records': login_record}})
        except Exception as e:
            print(e)
            err = error(e)
        
        return err




