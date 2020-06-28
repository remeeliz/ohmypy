##################################################
## FileName: appconfig.py
##################################################
## Author: RDinmore
## Date: 2020.06.27
## Purpose: config
## Libs:
## Path:
##################################################

#!/usr/bin/env python
import os

SECRET_KEY = os.urandom(24)
UPLOAD_FOLDER = '/tmp'

s3 = {
    "key_id":"AKIAIAVBG2RLZBY3PXWQ",
    "secret_key":"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",
    "region":"us-east-2",
    "bucket_name":"ohmypy-summer2020"}

use_anonymous = True