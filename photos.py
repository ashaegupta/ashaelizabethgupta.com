from flask import Flask, json, request
from instagram import client
from pictures.model.Photo import Photo
import local_settings
import simplejson


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
        process_instagram_post(request.data)

def process_instagram_post(rdata):
    json_data = simplejson.loads(rdata)
    data = json_data.get('data')
    if data:
        for d in data:
            # what's the type of the object?
            # get the object from instagram
            # save it in the database
            if d.get('object') == 'user' and d.get('changed_aspect') == 'media':
                user_id = d.get('object_id')
                access_token = local_settings.access_tokens.get(user_id)
                api = client.InstagramAPI(access_token=access_token)
                min_timestamp = d.get('time')
                pages = api.user_recent_media(as_generator=True,
                                              return_json=True,
                                              min_timestamp=min_timestamp,
                                              max_pages=1000)
                while True:
                    try:
                        page = pages.next()
                    except StopIteration:
                        break
                    except Exception, e:
                        print "Exception while getting data from instagram: %s" % e
                    for p in page[0]:
                        Photo.update(p)
                        print "Saved a photo from user: %s" % user_id

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
