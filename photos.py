from flask import Flask, json, request
from pictures.model.Photo import Photo

app = Flask(__name__)

@app.route("/pictures/latest")
def get_pictures():
    return get_latest_pictures()

@app.route("/pictures/olderthan/<created_time>")
def get_pictures_older_than(created_time):
    return get_latest_pictures(older_than=created_time)

def get_latest_pictures(older_than=None):
    if older_than:
        photos = Photo.get_photos(older_than=older_than)
    else:
        photos = Photo.get_photos()
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
