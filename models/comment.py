from models import db
from uuid import uuid4
from datetime import datetime


class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Text, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    user_id = db.Column(db.Text, db.ForeignKey('users.id'),
                        nullable=False)
    song_id = db.Column(db.Text, db.ForeignKey('songs.id'),
                        nullable=False)

    def __init__(self, comment, user_id, song_id):
        self.id = uuid4().hex
        self.comment = comment
        self.user_id = user_id
        self.song_id = song_id
