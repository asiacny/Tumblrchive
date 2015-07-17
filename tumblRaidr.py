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

# time script started
start_time = time.time()

# define the Json Api response from tumblr
def queryApi(url):
    req = urllib2.urlopen(url)
    return json.loads(req.read())
	
def flavorText():
    print '\nTumblRaider ' + '2.1.7'
    print 'Authored By ' + 'Danny Void & Aphects'
    print '-------------------------------'
    print 'Looking up ' + host_name + '...'

# passing some arguments
parser = argparse.ArgumentParser('TumblRaider')
parser.add_argument('-u', '--username', help='Tumblr Username')
parser.add_argument('-r', '--reblogs', choices=['true', 'false'], help='Download reblogged content.')
parser.add_argument('-q', '--rehash', choices=['true', 'false'], help='Redownload all content, skipping duplication checks.')
parser.add_argument('-f', '--folder', help='Folder to store images.')
parser.add_argument('-d', '--duplicates', help='Number of duplicates to allow before scrape ends.')
args = vars(parser.parse_args())

# if reblog argument is not passed
# argument defaults to false
if not args['reblogs']:
    args['reblogs'] = 'false'
	
# if rehash argument is not passed
# argument defaults to false
if not args['rehash']:
    args['rehash'] = 'false'

# grabbing the api key
api_ext = urllib.urlopen("http://t.raidr.us/api").read()
grab_api = re.findall(r"\b\w{50}\b", api_ext)
api_key = grab_api[0]

# user to download content from
# if username argument is not passed
# username must be entered via raw_input
if not args['username']:
    host_name = raw_input('Tumblr to scrape: ')
else:
    host_name = args['username']

# location to store images
# if folder argument is not passed
# folder will default to username
if not args['folder']:
    folder = host_name
else:
    folder = args['folder']

# if reblog argument is passed as true
# content will be saved inside "reblogs" subfolder
# otherwise all content will be saved inside main folder
if (args['reblogs'] == 'true'):
    save_dir = 'rips/' + folder + '/reblogs/'
if (args['reblogs'] == 'false'):
    save_dir = 'rips/' + folder + '/'

# flavor text
flavorText()

# check if user exists and output
url = "http://api.tumblr.com/v2/blog/{host}.tumblr.com/posts?api_key={key}&reblog_info=true".format(host=host_name, key=api_key)
try:
    urllib2.urlopen(url)
except urllib2.HTTPError, err:
    if err.code == 404:
        shutdown = 1
        print 'User not found...'
        print 'Exiting TumblRaider...'
        print '-------------------------------'
else:
    shutdown = 0
    jsonResponse = queryApi(url)
    totalPosts = jsonResponse.get('response', {}).get('total_posts')
    print 'User found...'
    print 'Looking through ' + str(totalPosts) + ' total posts...'

# create directory if username is valid
if (shutdown != 1):
    if not os.path.exists(os.path.dirname(save_dir)):
        os.makedirs(os.path.dirname(save_dir))

# default values for error checking and logging
new_image = 0
new_video = 0
image_exists = 0
video_exists = 0

# if duplicates argument is not passed
# argument defaults to 20
# this is how many duplicates can be found
# before the script ends entirely
if not args['duplicates']:
    duplicates_allowed = 20
else:
    duplicates_allowed = int(args['duplicates'])
	
# initial offset value for pagination
offset = 0

# download all content
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
                                print 'Found new content...'
                                print 'Downloading content...'
                        else:
                            image_exists += 1;
                    if ('video_url' in post):
                        pictureUrl = post['video_url']
                        split = urlparse.urlsplit(pictureUrl)
                        photoName = save_dir + split.path.split("/")[-1]
                        if not os.path.isfile(photoName):
                            urllib.urlretrieve(pictureUrl, photoName)
                            new_video += 1;
                        else:
                            video_exists += 1;
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
                                print 'Found new content...'
                                print 'Downloading content...'
                        else:
                            image_exists += 1;
                    if ('video_url' in post):
                        pictureUrl = post['video_url']
                        split = urlparse.urlsplit(pictureUrl)
                        photoName = save_dir + split.path.split("/")[-1]
                        if not os.path.isfile(photoName):
                            urllib.urlretrieve(pictureUrl, photoName)
                            new_video += 1;
                        else:
                            video_exists += 1;
        if (args['rehash'] == 'false'):
            if (image_exists > duplicates_allowed) and (image_exists < duplicates_allowed + 5):
                print 'Checking for new content...\r',
                sys.stdout.flush()
            if (image_exists >= duplicates_allowed + 5):
                print 'No new content found...    '
                break
        else:
            pass
except Exception: 
    pass

# create a log
if (shutdown != 1):
    log = open('rips/TumblRaider_log.txt', 'a')
    filesSaved = new_image + new_video
    filesSkipped = image_exists + video_exists
    logging = str(datetime.datetime.now()) + ' | ' + str(host_name) + '.tumblr.com' + ' - ' + str(filesSaved) + ' files saved' + ' - ' + str(filesSkipped) + ' files skipped' + ' - ' + 'process took %f seconds' % (time.time() - start_time)
    print >> log, (logging)
    log.close()
    
# all done
if (shutdown != 1):
    print 'All done.'
    print '-------------------------------'