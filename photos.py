from flask import Flask, json, request
from pictures.model.Photo import Photo

app = Flask(__name__)

### routes for Instagram's real time POSTs
@app.route("/pictures/instagram/sub", methods=['GET', 'POST'])
def instagram_sub():
    if request.method == 'GET':
        #mode = request.args.get('hub.mode')
        challenge = request.args.get('hub.challenge')
        #verify_token = request.args.get('hub.verify_token')
        return challenge
    elif request.method == 'POST':
        try: 
            print request.__dict__
            print '\n\n'
            print str(request.data)
            
        except: pass


### routes for the client to GET pictures json
@app.route("/pictures/latest")
def get_pictures():
    return get_latest_pictures()

@app.route("/pictures/olderthan/<created_time>")
def get_pictures_older_than(created_time):
    return get_latest_pictures(older_than=created_time)

@app.route("/pictures/newerthan/<created_time>")
def get_pictures_newer_than(created_time):
    return get_latest_pictures(newer_than=created_time)

@app.route("/pictures/around/<created_time>")
def get_pictures_around(created_time):
    return get_latest_pictures(around=created_time)

def get_latest_pictures(older_than=None, newer_than=None, around=None):
    if older_than:
        photos = Photo.get_photos(older_than=older_than)
    elif newer_than:
        photos = Photo.get_photos(newer_than=newer_than)
    elif around:
        photos = Photo.get_photos(around=around)
    else:
        photos = Photo.get_photos()

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
