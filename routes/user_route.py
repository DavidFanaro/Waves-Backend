from app import app, db
from models import User
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/api/v1/user/register', methods=['POST'])
def register():
    json = request.get_json()

    first_name = json['firstname']
    last_name = json['lastname']
    email = json['email']
    hash_pass = generate_password_hash(
        json['password'], method="sha256", salt_length=8)

    user = User(first_name, last_name, email, hash_pass)

    db.session.add(user)
    db.session.commit()

    return {
        'name': first_name + " " + last_name,
        'email': email
    },201


@app.route('/api/v1/user/login', methods=['POST'])
def login():
    json = request.get_json()
    email = json['email']
    password = json['password']

    user = User.query.filter_by(email = email).first()

    if check_password_hash(user.password, password):
        return{
            "id": user.id,
            "name": user.first_name + " " + user.last_name,
            'email': user.email
        },202
    return{
        'error': True,
        'message': "Wrong password"
    },404