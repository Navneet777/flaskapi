from flask import Flask, request, jsonify, make_response,Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
# from flaskext.mysql import MySQL
from flask_rest_paginate import Pagination
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/flaskapi'
db = SQLAlchemy(app)
errors = Blueprint('errors', __name__)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(20))
    Description = db.Column(db.String(100))
    Status = db.Column(db.String(20))
    Userid = db.Column(db.Integer)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,Name,Description,Status,Userid):

        self.Name = Name
        self.Userid = Userid
        self.Description = Description
        self.Status = Status
    def __repr__(self):
        return '' % self.id
db.create_all()

class TaskSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Task
        sqla_session = db.session
        Name = fields.String(required=True)
        Description = fields.String(required=True)
        Status = fields.String(required=True)
        Userid = fields.Number(required=True)

@app.route('/', methods = ['GET'])
def index():
    try:
        get_task = Task.query.all()
        task_schema = TaskSchema(many=True)
        task = task_schema.dump(get_task)
        if get_task is None:
            return make_response(jsonify({"status": "failure","error": "404","message":" Record Not Found"})),404
        else:
            return make_response(jsonify({"task": task}))
    except:
        return make_response(jsonify({"status": "failure","error": "404","message":"Not Found"})),404
@app.route('/<id>', methods = ['GET'])
def get_task_by_id(id):
    try:
        get_task = Task.query.get(id)
        task_schema = TaskSchema()
        task = task_schema.dump(get_task)
        if get_task is None:
            return make_response(jsonify({"status": "failure","error": "404","message":" Record Not Found"})),404
        else:
            return make_response(jsonify({"task": task}))
    except:
        return make_response(jsonify({"status": "failure","error": "404","message":"Not Found"})),404

@app.route('/delete/<id>', methods = ['DELETE'])
def delete_task_by_id(id):
    try:
        get_task = Task.query.get(id)
        db.session.delete(get_task)
        db.session.commit()
        if get_task is None:
            return make_response(jsonify({"status": "failure","error": "404","message":" Record Not Found"})),404
        else:
            return make_response(jsonify({"status": "success","message":" Record Delete Successfully"})),204
    except:
        return make_response(jsonify({"status": "failure","error": "404","message":" Record Not Found"})),404

@app.route('/post', methods = ['POST'])
def create_task():
    try:
        data = request.get_json()
        task_schema = TaskSchema()
        task = task_schema.loads(json.dumps(data))
        result = task_schema.dump(task.create())
        return make_response(jsonify({"task": result}),200)
    except:
        return make_response(jsonify({"status": "failure","error": "400","message":"Bad Request please input valid fields."})),400

@app.route('/update/<id>', methods = ['POST'])
def update_task_by_id(id):
    data = request.get_json()
    get_task = Task.query.get(id)
    if get_task is None:
        return make_response(jsonify({"status": "failure","error": "400","message":"Bad Request Record not found."})),400
    else:
        if data.get('Name'):
            get_task.Name = data['Name']
        if data.get('Description'):
            get_task.Description = data['Description']
        if data.get('Status'):
            get_task.Status = data['Status']
        if data.get('Userid'):
            get_task.Userid= data['Userid']
        db.session.add(get_task)
        db.session.commit()
        task_schema = TaskSchema(only=['id', 'Name', 'Description','Status','Userid'])
        task = task_schema.dump(get_task)
        return make_response(jsonify({"task": task,"status":"200","message":"record successfully updated"}))

@app.route('/pending', methods = ['GET'])
def pending_task():
    get_task = Task.query.filter_by(Status='pending')
    if get_task is None:
        return make_response(jsonify({"status": "failure","error": "400","message":"No pending tasks."})),400
    else:
        task_schema = TaskSchema(many=True)
        task = task_schema.dump(get_task)
        return make_response(jsonify({"status":"200","message":"pending tasks","task": task}))

@app.route('/complete', methods = ['GET'])
def complete_task():

    get_task = Task.query.filter_by(Status='complete')
    if get_task == None:
        return make_response(jsonify({"status": "failure","error": "400","message":"No complete tasks."})),400
    else:
        task_schema = TaskSchema(many=True)
        task = task_schema.dump(get_task)
        return make_response(jsonify({"status":"sucess","message":"complete tasks","task": task}))

@app.route('/pagination',methods=['GET'])
@app.route('/pagination/<int:page>',methods=['GET'])
def pagination(page=1):
    per_page = 5
    get_task = Task.query.paginate(page,per_page,error_out=False)
    task_schema = TaskSchema(many=True)
    task = task_schema.dump(get_task.items)
    return make_response(jsonify({"task": task}))

if __name__ == "__main__":
    app.run(debug=True)
