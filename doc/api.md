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
  
  **-- Role --**
  
  * anonymous：for login page & call data api
  * user：user api
  * admin：admin api
  
  **-- Permission --**

* **auths**

  ~~~json
  {
    uid: "1621231", // [PRIMARY_KEY] str
    role: 1, // 1=user || 2=admin
    
    identity_type: "email|google", // str
    identifier: "", // str
    credential: "", // str
    check_policy: true, // bool
    created_datetime: "" // str
  }
  ~~~

* **users**：註冊活動管理的使用者

  ~~~json
  {
    uid: "1621231", // [FOREIGN_KEY] str
    nickname: "jenson", // [PRIMARY_KEY] str
    avatar: "" // str 相片網址,
  }
  ~~~

* **line_users**

  ~~~json
  {
    "line_id": "", // {str} line user id
    "category": "official" || "beta", // official帳號或beta帳號
    "flag": "init", // 對話情境狀態
    "events": [], // {int-array} 參與活動的id
    
    "created_time": "", // {str} 加入時間
  }
  ~~~

* **login_records**

  ~~~json
  uid: "1621231", // str
  lastest_login_ip: "", // str 上一次login的ip位置
  lastest_login_time: "", // datetime, 上一次login的時間
  records: [{
    ip: "",
    time: "",
    isChange: false, // 是否有從不同ip位置登入
  }]
  ~~~

* **events**

  ~~~json
  id: "5124", // [PRIMARY_KEY] {str} 活動id
  owner_id: "1621231", // [FOREIGN_KEY] {str} 擁有活動的user id
  name: "", // {str}
  description: "", // {str}
  start_datetime: "", // {str}
  end_datetime: "", // {str}
  active: false, // {bool}
  
  setting: { // open function setting
    userSpecifiedOption: false, // {bool} 不能任意加入, 需有符合特定名單
    teamOption: false,  // {bool} 建立team, 點名等功能
    courseOption: false, // {bool} 課程
    playGroundOption: false // {bool} 闖關活動
  },
  
  users: {
    evu_id: "1523", // [PRIMARY_KEY] {str} 已報名此活動的使用者id
    name: "", 
  }
  ~~~

* **event_users**

  ~~~json
  event_id: "5124" // [FOREIGN_KEY] {str} 活動id
  line_id: "", // [FOREIGN_KEY] {str} user line id
  ~~~

  





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

  | API URL                     | API Method | Desc                 | Req Params                                                   | Resp Result                  |
  | --------------------------- | ---------- | -------------------- | ------------------------------------------------------------ | ---------------------------- |
  | v1URL/auth/check-identifier | GET        | 是否有重複identifier | identifier                                                   |                              |
  | v1URL/auth/check-nickname   | GET        | 是否重複nickname     | nickname                                                     |                              |
  | v1URL/auth/signup           | POST       | 註冊                 | identify_type, identifier, credential, check_policy, nickname, avatar |                              |
  | v1URL/auth/google-signup    | POST       | google auth註冊      | id_token, identify_type, nickname, avatar                    |                              |
  | v1URL/auth/login            | POST       | 登入                 | identifier, credential                                       | uid, role,  avatar, nickname |
  | v1URL/auth/google-login     | POST       | 登入                 | id_token                                                     | uid, role,  avatar, nickname |
  | v1URL/auth/logout           | POST       | 登出                 |                                                              |                              |


