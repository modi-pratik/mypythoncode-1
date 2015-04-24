__author__ = 'arc'

def validatephoto(request, photo_type=None):
    ''' create function here for validatephoto confirm
     in which parameter the base64 string is coming '''
    # import ipdb
    # ipdb.set_trace()
    # import PIL.Image
    import cStringIO
    from wand.image import Image

    error = dict()
    img_type, file_like = None, None
    img_base64data = request.values.get('image')
    if img_base64data:
        img_decoded = img_base64data.decode('base64')
        file_like = cStringIO.StringIO(img_decoded)
        img = Image(file=file_like)
        img_type = img.mimetype
        img_file_size = file_like.tell()
        image_info = img.size

        format_set = ('image/gif', 'image/jpeg', 'image/pjpeg', 'image/x-png', 'image/png', 'image/jpg')
        if img_type in format_set:
            width, height = image_info
            if photo_type == "cover":
                if width < 1500 or height < 400:
                    error['image'] = ['0 :The image uploaded is too small. Minimum size'
                                      ' required is width of 1500 and height of 400.']
            else:
                if width < 200 or height < 200:
                    error['image'] = ["0 : The image uploaded is too small. Minimum size required is 200 x 200. "]

                elif img_file_size > (2 * 1024 * 1024):
                    error['image'] = ['0 :Image size should be 2MB or less.']

        else:
            error['image'] = ['0 : Only jpg, jpeg, png, gif formats are allowed']
    else:
        error['image'] = ['0 : Only jpg, jpeg, png, gif formats are allowed']

    return {'error': error, 'img_type': img_type, 'file_like': file_like}


def uploadImage(file_like, filename, mimetype):
    ''' send file to s3 bucket '''
    import boto
    # import ipdb
    # ipdb.set_trace()
    from boto.s3.key import Key
    from boto.s3.connection import S3Connection
    from config_data import accessKeyID, secretAccessKey

    try:
        conn = S3Connection(accessKeyID, secretAccessKey)

        bucket = conn.get_bucket('workmob-dev')

        img_s3 = Key(bucket)
        img_s3.key = filename
        img_s3.content_type = mimetype
        file_like.seek(0)

        img_s3.set_contents_from_file(file_like)
        return True
    except:
        print "error in uploading file to server"
        return False


def unlinking(uid, type=None):

    imagecachepath = "files/imagecache"

    if not type:
        full_path = imagecachepath + "/" + type


