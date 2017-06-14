from flask import Flask, request, redirect, render_template, session, flash, url_for
from mysqlconnection import MySQLConnector
import re
import md5
import datetime
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key='secrets'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('^[^0-9]+$')
PASSWORD_REGEX = re.compile('\d.*[A-Z]|[A-Z].*\d')
mysql = MySQLConnector(app,'users3')

@app.route('/users')
def index():
    query = "SELECT * FROM users"
    users= mysql.query_db(query)
    print users
    return render_template('index.html', all_users = users)

@app.route('/users/new')
def new():
    return render_template('new.html')

@app.route('/users/<id>/edit')
def edit(id):
    return render_template('edit.html', id=id)

@app.route('/users/<id>')
def show(id):
    query = "SELECT id, first_name, last_name, email, DATE_FORMAT(created_at, '%M %D, %Y') as created  FROM users WHERE id = :id"
    data = { "id": id  }
    user = mysql.query_db(query, data)
    return render_template('show.html', user = user)

@app.route('/create', methods=['POST'])
def create():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first, :last, :email, NOW(), NOW())"
    data = {
        "first" : request.form['first'],
        "last": request.form['last'],
        "email": request.form['email']
    }
    mysql.query_db(query,data)
    query2 = "SELECT id FROM users WHERE email = :email"
    data2 = {"email": request.form['email']}
    user = mysql.query_db(query2,data2)
    id = user[0]['id']
    return redirect(url_for('show', id=id))

@app.route('/users/<id>/destroy')
def destroy(id):
    return redirect('/users')

@app.route('/update', methods =['POST'])
def update():
    query = "UPDATE users SET first_name = :first, last_name = :last, email = :email WHERE id = :id"
    data = {
        "first": request.form['first'],
        "last": request.form['last'],
        "email": request.form['email'],
        "id": request.form['id']
    }
    mysql.query_db(query,data)
    id= request.form['id']
    return redirect(url_for('show', id=id))

app.run(debug=True)