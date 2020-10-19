from models import db
from uuid import uuid4
from datetime import datetime


class Song(db.Model):

    __tablename__ = 'songs'

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(50), nullable=False)
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Text, db.ForeignKey(
        'users.id'), default=None, nullable=False)

    def __init__(self, name, desc, url, user_id):
        self.id = uuid4().hex
        self.name = name
        self.desc = desc
        self.url = url
        self.user_id = user_id
