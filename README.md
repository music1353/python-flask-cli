# Python Flask Cli

A backend structure based on Python Flask



## Requirements

~~~
flask
gunicorn
gevent
flask_sqlalchemy
flask_migrate
psycopg2-binary
~~~



## Get Started

* init database

  ~~~bash
  $ flask db init
  $ flask db migrate
  $ flask db upgrade
  ~~~

* run server

  ~~~bash
  $ export FLASK_APP=run.py
  $ flask run
  ~~~



