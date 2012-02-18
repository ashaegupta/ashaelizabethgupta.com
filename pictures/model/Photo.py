from collections import defaultdict
from pictures.model.MongoMixIn import MongoMixIn
from pymongo import DESCENDING

class Photo(MongoMixIn):
    MONGO_DB_NAME = 'photos'
    MONGO_COLLECTION_NAME = 'photo_collection'

    A_ID                = 'id'
    A_CREATED_TIME      = 'created_time'

    @classmethod
    def setup_mongo_indexes(klass):
        klass.mdbc().ensure_index([(klass.A_ID, DESCENDING)], unique=True)
        klass.mdbc().ensure_index([(klass.A_CREATED_TIME, DESCENDING)], unique=False)

    @classmethod
    def find_by_id(klass, id):
        return klass.mdbc().find_one({klass.A_ID: id})

    @classmethod
    def get_photos(klass, around=None, older_than=None, newer_than=None, limit=20, return_list=True):
        if around:
            above = klass.mdbc().find({klass.A_CREATED_TIME:{"$gte":around}}).sort(klass.A_CREATED_TIME).limit(limit/2)
            result = [a for a in above]
            print len(result), above.count()
            below = klass.mdbc().find({klass.A_CREATED_TIME:{"$lt":around}}).limit(limit/2)
            result += [b for b in below]
            print len(result), below.count()
            result.sort(key = lambda x: x.get(klass.A_CREATED_TIME), reverse=True)
            return result

        query = defaultdict(dict)
        if older_than and newer_than and older_than > newer_than:
            return []
        if older_than:
            query[klass.A_CREATED_TIME].update({"$lt":older_than})
        if newer_than:
            query[klass.A_CREATED_TIME].update({"$gt":newer_than})
        cursor = klass.mdbc().find(query).sort(klass.A_CREATED_TIME, DESCENDING).limit(limit)
        return [l for l in cursor]

    @classmethod
    def format_photos_for_api(klass, photos):
        """strips out keys we don't want from photos.
        the keys we want are specified in 'keys_for_api'
        """
        formatted_photos = []
        keys_for_api = {
            'caption':{'text':1},
            'created_time':1,
            'filter':1,
            'id':1,
            'images':{'standard_resolution':{'url':1}},
            'link':1,
            'likes':{'count':1}
        }
        for p in photos:
            f_photos = klass._get_keys_from_hash(keys_for_api, p)
            formatted_photos.append(f_photos)
        return formatted_photos

    @classmethod
    def _get_keys_from_hash(klass, keys, hash):
        """recursively creates a dictionary of the values we want to keep,
        which are specified in 'keys', from the dict 'hash'
        """
        f_photo = {}
        for k, v in keys.iteritems():
            if k in hash:
                if isinstance(hash[k], dict) and isinstance(keys[k], dict):
                    f_photo[k] = klass._get_keys_from_hash(keys[k], hash[k])
                else:
                    f_photo[k] = hash[k]
        return f_photo

    @classmethod
    def update(klass, doc):
        id = doc.get(klass.A_ID)
        spec = {klass.A_ID: id}
        document = {"$set": doc}
        return klass.mdbc().update(spec=spec, document=document, upsert=True, safe=True)
        
