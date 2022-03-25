# NAMA KELOMPOK :
# 1. HANIFAN HUSEIN ISNANTO (19090006)
# 2. MUHAMMAD FIKRI (19090126)
# KELAS : 6 C

import os, random, string

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json 
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class User(db.Model):
  username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
  password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
  token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)

db.create_all()

# POST http://127.0.0.1:8080/addUser -d '{"username": "19090006", "password": "123", "token": ""}'
@app.route("/addUser", methods=["POST"])
def add_user():
  username = request.form['username']
  password = request.form['password']

  dataUser = User(username=username, password=password)
  db.session.add(dataUser)
  db.session.commit() 
  return jsonify({
    'msg': 'User berhasil ditambahkan',
    'status': 200 
  })

# POST http://127.0.0.1:8080/api/v1/login -d '{"username": "19090006", "password": "123"}'
@app.route("/api/v1/login", methods=["POST"])
def login():
  username = request.form['username']
  password = request.form['password']

  user = User.query.filter_by(username=username, password=password).first()

  if user:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    User.query.filter_by(username=username, password=password).update({'token': token})
    db.session.commit()
    return jsonify({
      'msg': 'Login berhasil',
      'token': token,
      'status': 200 
    })
  else:
    return jsonify({
      'msg': 'Login gagal'
    })

# POST http://127.0.0.1:8080/api/v2/users/info -d '{"token": "sesuaikan dengan token yang aktif"}'
@app.route("/api/v2/users/info", methods=["POST"])
def info():
  token = request.values.get('token')
  user = User.query.filter_by(token=token).first()
  if user:
    return jsonify({
      'username': user.username,
      'status': 200
      })
  else:
    return jsonify({
      'msg': 'Token salah'
      })

if __name__ == '__main__':
  app.run(debug = True, port=8080)

