from flask import Flask, json
from pictures.model.Photo import Photo

app = Flask(__name__)

@app.route("/pictures/<id>")
def get_picture_with_id(id):
    return get_latest_pictures(id=id)

@app.route("/pictures")
def get_pictures():
    return get_latest_pictures(id=None)

def get_latest_pictures(id=None):
    if id == 'latest':
        photos = Photo.get_photos()
    else:
        photos = Photo.get_photos(around=id)
    formatted_photos = Photo.format_photos_for_api(photos)
    return json.dumps(formatted_photos)

if __name__ == '__main__':
    app.run(debug=True)
