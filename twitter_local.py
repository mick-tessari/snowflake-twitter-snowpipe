#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Future modules for Python 2
from __future__ import print_function

# Built-in modules
import sys
import os
import json

# Third-party modules
import boto3
import tweepy
from datetime import datetime

__author__ = "Michele Tessari"
__version__ = "1.0"
__maintainer__ = "Michele Tessari"
__email__ = "michele.tessari@snowflake.com"
__status__ = "Prototype"

# Twitter authentication for Tweepy
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# Global variables
s3_client = boto3.client('s3')
tweet_list = []
total_count = 0

class JSONStreamProducer(tweepy.StreamListener):

    def __init__(self, s3_client):
        super(tweepy.StreamListener, self).__init__()
        self.s3_client = s3_client

    def on_data(self, data):
        global tweet_list
        global total_count
        data_dict = json.loads(data)
        data_dict.update({"keyword":keyword})
        tweet_list.append(json.dumps(data_dict))
        total_count += 1
        if total_count % 2 == 0:
            print(".", end="")
            sys.stdout.flush()
        if total_count % 100 == 0:
            print("{0} tweets retrieved".format(str(total_count)))
            filename = 'tweets_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.json'
            print("==> writing " + str(len(tweet_list)) + " records to " + filename)
            tweet_file = open(filename, 'w')
            tweet_file.writelines(tweet_list)
            tweet_file.close()
            print("==> uploading file to S3...")
            sys.stdout.flush()
            now = datetime.now()
            key = "{0}/{1}/{2}/{3}/{4}/{5}/{6}".format(keyword, str(now.year), str(now.month), str(now.day),str(now.hour), str(now.minute), filename)
            print("==> uploading to " + key)
            s3_client.upload_file(filename, bucket, key)
            print("==> file uploaded to " + key)
            tweet_list = []
            os.remove(filename)
        return True

    def on_error(self, status):
        print("Error: " + str(status))


def main():
    global bucket
    global keyword
    consumer_key = sys.argv[1]
    consumer_secret = sys.argv[2]
    access_token = sys.argv[3]
    access_token_secret = sys.argv[4]
    bucket = sys.argv[5]
    keyword = "#"+sys.argv[6]

    global auth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    mylistener = JSONStreamProducer(s3_client)
    myStream = tweepy.Stream(auth=auth, listener=mylistener)
    myStream.filter(track=[keyword])


if __name__ == "__main__":
    main()
