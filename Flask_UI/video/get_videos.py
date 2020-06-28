import sys
sys.path.append("..")
from filestore import *

aws_path = "https://ohmypy-summer2020.s3.amazonaws.com/"
videolist = get_s3objectList("videos/")

for video in videolist["Key"]:
    print(aws_path + video)