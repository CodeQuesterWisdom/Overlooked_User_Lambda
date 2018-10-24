
import base64
import json
import boto
from base64 import decodestring
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection

import boto.s3.connection


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def remove_prefix(encodedImage):
    firstComma = encodedImage.find(',')
    firstComma = firstComma + 1
    noPrefix = encodedImage[firstComma:]
    return noPrefix

def getFileExtension(encodedImage):
    # take characters between / and ;
    fileExtension = find_between(encodedImage, "/", ";")
    if fileExtension == "":
        fileExtension = ".jpg"
    else:
        fileExtension = fileExtension
    # print(fileExtension)
    return fileExtension


def image_handler(firebaseID, encodedImage): #encoded_img -> param :
    try:
        # with open('test_images/image2.png','rb') as f:
        #     data = f.read()
        #     encodedImage = base64.b64encode(data)
        # ^^ IF THIS IS UNCOMMENTED, ALL CODE BELOW NEEDS TO INDENT 1 TAB
        fileExtension = getFileExtension(encodedImage)
        encodedImage = remove_prefix(encodedImage)
        decodedImage = base64.b64decode(encodedImage)
        # print(decodedImage.format)
        AWS_ACCESS_KEY_ID = 'AKIAJNP5MTZJYBDXMQNA'
        AWS_SECRET_KEY_ID = '96Ajv3F0s0mDZmDN5b78X8HRWzrokBpF538sPrUq'

        conn = boto.s3.connect_to_region('us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY_ID,
        is_secure=True,
        calling_format=OrdinaryCallingFormat(),
        )

        bucket_name = 'overlooked-upload-test'
        bucket = conn.get_bucket(bucket_name)
        k = Key(bucket)
        folder_name = 'profilePics'

        # filename = str("test"+".jpg")
        filename = str(firebaseID+"."+fileExtension)
        k.key = folder_name +"/"+filename
        k.set_contents_from_string(decodedImage)
        # content_type = 'image/' + fileExtension
        if fileExtension == 'jpg':
            k.set_metadata('Content-Type', 'image/jpg')
            # k.content_type = 'image/jpg'
        elif fileExtension == 'png':
            k.set_metadata('Content-Type', 'image/png')
            # k.content_type = 'image/png'
        elif fileExtension == 'jpeg':
            k.set_metadata('Content-Type', 'image/jpeg')
            # k.content_type = 'image/jpeg'
        else:
            k.set_metadata('Content-Type', 'image/jpg')
            # k.content_type = 'image/jpeg'

        k.set_acl('public-read')


        # content_type = 'image/' + fileExtension
        # bucket.put_object(Key=filename, Body=decodedImage, ContentType=content_type, ACL='public-read')
        # bucket.upload_file()
        # s3url = k.generate_url(expires_in=1000)
        baseS3URL = 'https://s3-us-west-1.amazonaws.com/'
        fullS3URL = baseS3URL  + bucket_name + "/" + folder_name + "/" + filename
        # print(s3url)

        return fullS3URL

    except:
        errMsg = "error"
        print(errMsg)
        return errMsg




# encodedImage ="data:image/png;base64,iVBORwiwq2AsWrOgqiKJrAWSxYVcWAXt9WFB"
# remove_prefix(encodedImage)
# getFileExtension("data:image/png;base64,iVBORw0KGgo/AAAANS;UhEUgAAAe4AAAHm")
# image_handler()
