#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import certifi
import os
import subprocess


__author__ = "Michele Tessari"
__version__ = "1.0"
__maintainer__ = "Michele Tessari"
__email__ = "michele.tessari@snowflake.com"
__status__ = "Prototype"


# Adding Netskope certificates to Certifi
cafile = certifi.where()
certpath = 'cert.pem'
with open(certpath, 'rb') as infile:
    customca = infile.read()
with open(cafile, 'ab') as outfile:
    outfile.write(customca)
print('==> Certificates added to Certifi.')
os.remove(certpath)
