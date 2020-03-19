#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Future modules for Python 2
from __future__ import print_function

import json
import os
import queue

# Built-in modules
import sys
import threading
import time
from datetime import datetime

# Third-party modules
import boto3
import tweepy

__author__ = "Michele Tessari"
__version__ = "1.0"
__maintainer__ = "Michele Tessari"
__email__ = "michele.tessari@snowflake.com"
__status__ = "Prototype"


def consumer(pipe, ev):

    tweet_list = []
    total_count = 0
    s3_client = boto3.client('s3')

    while not ev.is_set() or not pipe.empty():

        data = pipe.get()
        data_dict = json.loads(data)
        data_dict.update({"keyword": keyword})
        tweet_list.append(json.dumps(data_dict))
        total_count += 1

        if total_count % 2 == 0:
            print(".", end="")
            sys.stdout.flush()
        if total_count % 100 == 0:
            print("{0} tweets retrieved".format(str(total_count)))
            sys.stdout.flush()
            filename = 'tweets_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.json'
            print("==> writing " + str(len(tweet_list)) + " records to " + filename)
            sys.stdout.flush()
            tweet_file = open(filename, 'w')
            tweet_file.writelines(tweet_list)
            tweet_file.close()
            now = datetime.now()
            key = "{0}/{1}/{2}/{3}/{4}/{5}/{6}".format(keyword, str(now.year), str(now.month), str(now.day),
                                                       str(now.hour), str(now.minute), filename)
            print("==> uploading to " + key)
            sys.stdout.flush()
            s3_client.upload_file(filename, bucket, key)
            print("==> uploaded to " + key)
            sys.stdout.flush()
            tweet_list = []
            os.remove(filename)


class JSONStreamProducer(tweepy.StreamListener):

    def on_data(self, data):
        pipeline.put(data)
        if not event.is_set():
            return True
        else:
            return False

    def on_error(self, status):
        print("Error: " + str(status))


def on_press():

    event.set()


if __name__ == "__main__":

    consumer_key = sys.argv[1]
    consumer_secret = sys.argv[2]
    access_token = sys.argv[3]
    access_token_secret = sys.argv[4]
    bucket = sys.argv[5]
    keyword = "#" + sys.argv[6]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    pipeline = queue.Queue()
    event = threading.Event()

    myListener = JSONStreamProducer()
    myStream = tweepy.Stream(auth=auth, listener=myListener)
    myStream.filter(track=[keyword], is_async=True)

    t = threading.Thread(target=consumer, args=(pipeline, event))
    t.start()

    # setting a safety 15-min timeout
    time.sleep(900)
    event.set()
