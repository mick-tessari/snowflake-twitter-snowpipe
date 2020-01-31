#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Future modules for Python 2
from __future__ import print_function

# Built-in modules
import sys
import os

# Third-party modules
import boto3
import tweepy
from datetime import datetime

__author__ = "Michele Tessari"
__version__ = "1.0"
__maintainer__ = "Michele Tessari"
__email__ = "michele.tessari@snowflake.com"
__status__ = "Prototype"

# Insert your Twitter Developer app keys and tokens here
consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Twitter authentication for Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Global variables
s3_client = boto3.client('s3')
tweet_list = []
total_count = 0
bucket = 'snowpipe-local'


def usage():
    print("""\
# Usage: twitter_local.py keyword [s3_bucket_name]
""")


class JSONStreamProducer(tweepy.StreamListener):

    def __init__(self, s3_client):
        super(tweepy.StreamListener, self).__init__()
        self.s3_client = s3_client

    def on_data(self, data):
        global tweet_list
        global total_count
        tweet_list.append(data)
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
            key = "{0}/{1}/{2}/{3}/{4}/{5}/{6}/".format(bucket, str(now.year), str(now.month), str(now.day),
                                                        str(now.hour), str(now.minute), filename)
            s3_client.upload_file(filename, bucket, key)
            print("==> file uploaded to " + key)
            tweet_list = []
            os.remove(filename)
        return True

    def on_error(self, status):
        print("Error: " + str(status))


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    if len(sys.argv) > 2:
        global bucket
        bucket = sys.argv[2]

    keyword = sys.argv[1]

    mylistener = JSONStreamProducer(s3_client)
    myStream = tweepy.Stream(auth=auth, listener=mylistener)
    myStream.filter(track=[keyword])


if __name__ == "__main__":
    main()
