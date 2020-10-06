from models import db
from uuid import uuid4

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Text, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, first, last, email, password):
        self.id = uuid4().hex
        self.first_name = first
        self.last_name = last
        self.email = email
        self.password = password