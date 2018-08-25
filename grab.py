import json
import requests
import sys
import urllib
import os

base_url = None

def set_board():
    board = raw_input("What board do you want to scrape? (e.g. anime, technology, b): ");

    global base_url
    base_url = "https://a.4cdn.org/{}/catalog.json".format(board)

def set_folder():
    path = './images'

    if not os.path.exists(path):
        os.makedirs(path)
        print "Folder named 'images' created.."

def grab_images():
    set_board()
    set_folder()
    search = raw_input("What thread do you want to search for? (e.g. ylyl, fun): ")

    print("Grabbing all images from current 4chan {} threads...".format(search))

    r = requests.get(base_url)
    catalog_json = json.loads(r.text)

    most_posts = []

    for catalog in catalog_json:

        for thread in catalog['threads']:
            thread_no = thread['no']
            get_thread = requests.get("https://a.4cdn.org/b/thread/{}.json".format(thread_no))

            if (get_thread.status_code == 404):
                print("Reached end.. done!")
                return

            threads_json = json.loads(get_thread.text)

            title = threads_json['posts'][0]['semantic_url']

            print("Current thread: {}".format(title))

            if((search in title)):
                for post in threads_json['posts']:

                    if(post.get('ext')):
                        tim = post['tim']
                        ext = post['ext']
                        urllib.urlretrieve("https://i.4cdn.org/b/{}{}".format(tim, ext), "images/{}_{}{}".format(title, tim, ext))

                        print("{}_{}{} downloaded..\n".format(title, tim, ext))
    print("Done!")

grab_images()
