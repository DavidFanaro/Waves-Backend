from os import path
import os
import boto3

bucketName = os.environ.get("BUCKETNAME")
awsAccessKey = os.environ.get("AWSACCESSKEYID")
awsSecretKey = os.environ.get("AWSSECRETKEY")


boto3 = boto3.resource('s3', aws_access_key_id=awsAccessKey,
                      aws_secret_access_key=awsSecretKey)

bucket = boto3.Bucket(bucketName)



# basepath = path.dirname(__file__)
# filepath = path.abspath(path.join(basepath, "..", "uploads"))

# if path.isdir(filepath) is False:
#     print('created upload folder')
#     os.mkdir(filepath)
# else:
#     print('upload folder exist')

from app import app, db
from flask import request, render_template, send_file, url_for
from models import Song, User
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'mp3'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/v1/uploadsong', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email = email).first()

        if check_password_hash(user.password, password):

            if request.files is not None:
                f = request.files['file']
                if f and allowed_file(f.filename):

                    name = request.form['title']
                    desc = request.form['desc']
                    url = "https://waves-main-bucket.s3.us-east-2.amazonaws.com/" + f.filename

                    song = Song(name, desc, url, user.id)
                    db.session.add(song)
                    db.session.commit()

                    try:
                        bucket.Object(f.filename).put(ACL='public-read',Body=f)
                    except :
                        return "Unknown Error", 500
                    
                else:
                    return 'bad file type', 400
            else:
                return 'No file submited',400

        else:
            return "Failed to login",403

        return f'Thanks {user.first_name} for uploading a song',201
    else:
        return render_template('SongUpload.html')


@app.route('/api/v1/songs')
def Songs():
    songs = Song.query.all()

    if songs is not None:
        songdata = []

        for song in songs:
            user = User.query.filter_by(id = song.user_id).first()
            i = {
                "title": song.name,
                "desc": song.desc,
                "url": song.url,
                "user": user.first_name + " " + user.last_name
            }
            songdata.append(i)

        data = {'songs': songdata}

        return data,200

    return "No Songs found",404


@app.route('/api/v1/song/<id>')
def getSong(id):
    song = Song.query.filter_by(id = id).first()

    return send_file(song.url),200
