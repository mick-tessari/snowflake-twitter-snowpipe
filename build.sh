# Script version v1.0
# Author: Michele Tessari
# E-mail: michele.tessari@snowflake.com
#'
# README:
#

#!/bin/bash

security find-certificate -a -c skope -p > cert.pem
docker build --pull --no-cache -t sf-twitter .
rm cert.pem
