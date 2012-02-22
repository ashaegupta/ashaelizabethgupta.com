from flask import Flask, json, request
from pictures.model.Photo import Photo
from pictures.lib.PhotoSaver import PhotoSaver
from pictures import local_settings
import simplejson
import hmac
import hashlib

app = Flask(__name__)

### routes for Instagram's real time POSTs
@app.route("/pictures/instagram/sub", methods=['GET', 'POST'])
def instagram_sub():
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        return challenge
    elif request.method == 'POST':
        signature = request.headers.get('X-Hub-Signature')
        body = request.data
        if verify_instagram_post(signature, body):
            process_instagram_post(body)
        else:
            print "Could not verify instagram post"

def process_instagram_post(rdata):
    try:
        json_data = simplejson.loads(rdata)
        PhotoSaver.process_instagram_post(json_data)
    except Exception, e:
        print "Error trying to process instagram's post: %s, data: %s" % (
            e, rdata)

def verify_instagram_post(signature, body):
    client_secret = local_settings.client_secret
    digest = hmac.new(client_secret.encode('utf-8'),
                      msg = body.encode('utf-8'),
                      digestmod = hashlib.sha1
                     ).hexdigest()
    return digest == signature

### routes for the client to GET pictures json
@app.route("/pictures/<user_id>/latest")
def get_pictures(user_id):
    return get_latest_pictures(user_id)

@app.route("/pictures/<user_id>/olderthan/<created_time>")
def get_pictures_older_than(user_id, created_time):
    return get_latest_pictures(user_id, older_than=created_time)

@app.route("/pictures/<user_id>/newerthan/<created_time>")
def get_pictures_newer_than(user_id, created_time):
    return get_latest_pictures(user_id, newer_than=created_time)

@app.route("/pictures/<user_id>/around/<created_time>")
def get_pictures_around(user_id, created_time):
    return get_latest_pictures(user_id, around=created_time)

def get_latest_pictures(user_id, older_than=None, newer_than=None, around=None):
    if older_than:
        photos = Photo.get_photos(user_id, older_than=older_than)
    elif newer_than:
        photos = Photo.get_photos(user_id, newer_than=newer_than)
    elif around:
        photos = Photo.get_photos(user_id, around=around)
    else:
        photos = Photo.get_photos(user_id)

    # deal with a jsonp request
    callback = request.args.get('callback')
    formatted_photos = Photo.format_photos_for_api(photos)
    if callback:
        content = str(callback) + '(' + json.dumps(formatted_photos) + ');'
    else:
        content = json.dumps(formatted_photos)

    response = app.make_response(content)
    response.mimetype = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5002)
