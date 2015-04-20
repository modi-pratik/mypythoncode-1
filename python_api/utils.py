__author__ = 'arc'

def validatephoto(request):
    '''
    create function here for validatephoto confirm
     in which parameter the base64 string is coming
     '''
    import cStringIO
    import PIL.Image
    from wand.image import Image

    error = dict()
    img_binarydata = request.values['image']
    photo_type = request.values['type']
    file_like = cStringIO.StringIO(img_binarydata)
    img = Image(file=file_like)
    img_type = img.mimetype
    img_file_size = file_like.tell()
    image_info = img.size

    # encoded_image = base64.b64encode(img_binarydata)

    # UUU = base64.b64decode(img_base64data)
    # file_size = file_like.tell()
    # # img = PIL.Image.open(file_like)
    # img = Image(file=file_like)
    # image_type = img.mimetype

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
    # if error:
    #     return error
    return {'error': error, 'img_type': img_type, 'file_like': file_like}


def uploadImage(file_like):
    ''' send file to s3 bucket '''
    import boto
    from boto.s3.key import Key
    from boto.s3.connection import S3Connection

    conn = S3Connection('AKIAIQMFRF3T3OGGT63Q', 'pfNgxSW+ZVTNghluSAT24nMaZuFtmOli+Cjzinej')

    bucket = conn.get_bucket('workmob-dev')

    key_image = Key(bucket)
    try:
        key_image.send_file(file_like)
        return True
    except:
        print "error in uploading file to server"
        return False

def unlinking(uid, type=None):

    imagecachepath = "files/imagecache"

    if not type:
        full_path = imagecachepath + "/" + type
    