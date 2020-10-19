# 啟動伺服器

* Use Flask：`python run.py`
* Use Gunicorn：`gunicorn -w 4 -b 127.0.0.1:5000 run:app`
* Use waitress：`python server.py`



# MongoDB

* role

  ~~~json
  {
    "id": 0, // int
    "name": "anonymous|user|admin", // str
    "permission": 1 // int
  }
  ~~~
  
  **Role**
  
  * anonymous：for login page & call data api
  
  * user：user api
  * admin：admin api
  
  **Permission**
  
  * 



# Restful API

* v1URL = https://hostname:5000/api/v1

* **Response Format**

  ~~~python
  resp = {
    "msg": "",
    "result": ""
  }
  ~~~
  
* **Status Code**

  | Status Code | Description           |
  | ----------- | --------------------- |
  | 200         | OK                    |
  | 401         | Unauthorization       |
  | 400         | Bad Requests          |
  | 500         | Internal Server Error |

* **adminAPI**

  | API URL                     | API Method | Desc               | Req Params                           | Resp Result                                                  |
  | --------------------------- | ---------- | ------------------ | ------------------------------------ | ------------------------------------------------------------ |
  | v1URL/admin/auth/login      | POST       | 管理員登入         | account, password                    | name, account, auth(身份)                                    |
  | v1URL/admin/auth/login      | POST       | 管理員登出         |                                      |                                                              |
  | v1URL/admin/auth/checkLogin | GET        | 管理員檢查登入狀態 |                                      | `bool`status, auth, account                                  |
  | v1URL/admin/contact         | POST       | 新增一筆聯絡資料   | name, company, phone, email, content |                                                              |
  | v1URL/admin/contact/list    | GET        | 取得所有聯絡資料   |                                      | [{id, name, company, phone, email, content, create_datetime}] |
  |                             |            |                    |                                      |                                                              |


