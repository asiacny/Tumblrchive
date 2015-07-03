import os
import re
import sys
import json
import time
import urllib
import urllib2
import urlparse
import argparse
import datetime

# some boring time measurement
start_time = time.time()

# passing some arguments
parser = argparse.ArgumentParser('Raidr')
parser.add_argument('-u', '--username', help='Tumblr Username')
parser.add_argument('-r', '--reblogs', help='True enables the download of reblogged images. False just downloads unique, non-reblogged content.')
parser.add_argument('-f', '--folder', help='Folder to store images.')
parser.add_argument('-d', '--duplicates', help='Number of duplicates to allow before scrape ends.')
args = vars(parser.parse_args())

if not args['reblogs']:
    args['reblogs'] = 'false'

# grabbing the api key
api_ext = urllib.urlopen("http://t.raidr.us/api").read()
grab_api = re.findall(r"\b\w{50}\b", api_ext)
api_key = grab_api[0]

# user to scrape
if not args['username']:
    host_name = raw_input('Tumblr to scrape: ')
else:
    host_name = args['username']

# location to store images
if not args['folder']:
    folder = host_name
else:
    folder = args['folder']
    
if (args['reblogs'] == 'true'):
    save_dir = 'rips/' + folder + '/reblogs/'
if (args['reblogs'] == 'false'):
    save_dir = 'rips/' + folder + '/'

# current version, and authors
current_ver = '1.1.8'
authors = 'Aphects & DannyVoid'

# flavor text
print '\nRaidr ' + current_ver
print 'Authored By ' + authors
print '-------------------------------'
print 'Looking up ' + host_name + '...'

# retreiving json response from tumblr api
def queryApi(url):
    req = urllib2.urlopen(url)
    return json.loads(req.read())

# initial offset value
offset = 0

# initial url for first query
url = "http://api.tumblr.com/v2/blog/{host}.tumblr.com/posts?api_key={key}&reblog_info=true".format(
    host=host_name, key=api_key)

# create directory if it doesn't exist
if not os.path.exists(os.path.dirname(save_dir)):
    os.makedirs(os.path.dirname(save_dir))

# initial call the api used to test total posts
jsonResponse = queryApi(url)

# retrieves total posts
totalPosts = jsonResponse.get('response', {}).get('total_posts')

# shows total posts
print 'User found...'
print 'Looking through ' + str(totalPosts) + ' total posts...'

# duplicate and new image checking
image_exists = 0
new_image = 0
if not args['duplicates']:
    duplicates_allowed = 20
else:
    duplicates_allowed = int(args['duplicates'])

# download all images
try:
    while (not (offset >= totalPosts + 20)):
        url = "http://api.tumblr.com/v2/blog/{host}.tumblr.com/posts?api_key={key}&reblog_info=true&offset={offset}".format(
            host=host_name, key=api_key, offset=offset)
        offset += 20;
        jsonResponse = queryApi(url)
        posts = jsonResponse.get('response', {}).get('posts', {})
        for post in posts:
            if (args['reblogs'] == 'true'):
                if ('reblogged_from_id' in post):
                    photos = post.get('photos', {})
                    for photo in photos:
                        pictureUrl = photo.get('original_size', {}).get('url', '')
                        split = urlparse.urlsplit(pictureUrl)
                        photoName = save_dir + split.path.split("/")[-1]
                        if not os.path.isfile(photoName):
                            urllib.urlretrieve(pictureUrl, photoName)
                            new_image += 1;
                            if (new_image == 1):
                                print 'Found new images...'
                                print 'Downloading images...'
                        else:
                            image_exists += 1;
            if (args['reblogs'] == 'false'):
                if ('reblogged_from_id' not in post):
                    photos = post.get('photos', {})
                    for photo in photos:
                        pictureUrl = photo.get('original_size', {}).get('url', '')
                        split = urlparse.urlsplit(pictureUrl)
                        photoName = save_dir + split.path.split("/")[-1]
                        if not os.path.isfile(photoName):
                            urllib.urlretrieve(pictureUrl, photoName)
                            new_image += 1;
                            if (new_image == 1):
                                print 'Found new images...'
                                print 'Downloading images...'
                        else:
                            image_exists += 1;
        if (image_exists > duplicates_allowed) and (image_exists < duplicates_allowed + 5):
            print 'Checking for new images...'
        if (image_exists >= duplicates_allowed + 5):
            print 'No new images found...'
            break
except Exception: 
    pass

# create a log
log = open('rips/Raidr_log.txt', 'a')
logging = str(datetime.datetime.now()) + ' | ' + str(host_name) + '.tumblr.com' + ' | ' + str(new_image) + ' images saved' + ' | ' + str(image_exists) + ' images skipped' + ' | ' + 'process took %f seconds' % (time.time() - start_time)
print >> log, (logging)
log.close()
    
# all done
print 'All done.'
print '-------------------------------'