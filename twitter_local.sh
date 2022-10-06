# Script version v1.0
# Author: Michele Tessari
# E-mail: michele.tessari@snowflake.com
#'
# README:
#

#!/bin/bash

echo Keyword: \#${1:-${keyword}}
# python ./twitter_local.py $consumer_key $consumer_secret $access_token $access_token_secret $bucket ${1:-${keyword}} $twitter_bearer_token
python ./twitter_local.py $bucket ${1:-${keyword}} $twitter_bearer_token
