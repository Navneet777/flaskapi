from flask import Flask, request, jsonify, make_response,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flaskapi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

from sqlalchemy import text

sql = text('select name from penguins')
result = db.engine.execute(sql)
names = [row[0] for row in result]

@app.route('/', methods = ['GET'])
def index():
    get_task =

    task = task_schema.dump(get_task)
    return make_response(jsonify({"task": task}))
