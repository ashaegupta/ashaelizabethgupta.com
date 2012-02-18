import time
import local_settings
from instagram import client
access_token = local_settings.asha_access_token
api = client.InstagramAPI(access_token=access_token)
pages = api.user_recent_media(as_generator=True, return_json=True, max_pages=1000)

raw_responses = []
while True:
    try:
        page = pages.next()
    except StopIteration:
        break
    raw_response = page[0]
    print "got %d pictures" % len(raw_response)
    raw_responses.extend(raw_response)

api_response_file_name = 'api_response_%s.txt' % int(time.time())
print "saving %s raw responses to file: %s" % (len(raw_responses), 
                                               api_response_file_name)
api_response_file = open(api_response_file_name, 'w')
api_response_file.write(repr(raw_responses))
api_response_file.close()
print 'done'
