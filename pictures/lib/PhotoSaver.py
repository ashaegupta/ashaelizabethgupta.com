import local_settings
from pictures.model.Photo import Photo
from instagram import client

class PhotoSaver():
    
    @classmethod
    def process_instagram_post(klass, post_data):
        for d in post_data:
            if d.get('object') == 'user' and d.get('changed_aspect') == 'media':
                user_id = d.get('object_id')
                min_timestamp = d.get('time')
                klass.get_new_photos(user_id, min_timestamp)

    @classmethod
    def get_new_photos(klass, user_id, min_timestamp):
        access_token = local_settings.access_tokens.get(user_id)
        api = client.InstagramAPI(access_token=access_token)
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

