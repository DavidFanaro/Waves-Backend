from app import app, db
from flask import request, render_template
from models import User, Song, Comments

@app.route('/api/v1/comments', methods=['POST'])
def create_comments():

    if request.method == "POST":
        json = request.get_json()
        user_id = json['user_id']
        song_id = json['song_id']
        comment_text = json['comment']

        user = User.query.filter_by(id=user_id).first()
        song = Song.query.filter_by(id=song_id).first()
        comment = Comments(comment_text,user_id,song_id)

        db.session.add(comment)
        db.session.commit()

        return{
            "message": f'{user.first_name} added a comment to {song.name}'
        }
    return "failed to create comment"

@app.route('/api/v1/comments')
def getallComments():

    comments = Comments.query.all()

    parsed_comments = []

    for comment in comments:
        user = User.query.filter_by(id=comment.user_id).first()
        song = Song.query.filter_by(id=comment.song_id).first()

        parsed_comments.append({
            'comments': comment.comment,
            'user': f'{user.first_name} {user.last_name}',
            'song': song.name
        })

    return {
        "comments": parsed_comments
    }


@app.route('/api/v1/comments/song')
def getSongComments():

    json = request.get_json()

    song_id = json['song_id']

    comments = Comments.query.filter_by(song_id = song_id).all()

    song = Song.query.filter_by(id = song_id).first()

    parsed_comment = []

    for comment in comments:
        user = User.query.filter_by(id = comment.user_id).first()

        parsed_comment.append({
            'user': f'{user.first_name} {user.last_name}',
            'comment': comment.comment
        })

    return{
        'song': song.name,
        'comments': parsed_comment
    }

