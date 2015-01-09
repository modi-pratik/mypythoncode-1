import Image
import numpy as np
import glob


filename = '/home/stonex/imagefilepath'
image_list = glob.glob("/home/stonex/Pictures/*.jpg")
# import ipdb
# ipdb.set_trace()

size = 128, 128

# data = np.genfromtxt(filename, delimiter="\n", dtype="S")
counter = 1
total_count = len(image_list)
for row in image_list:
    print "processing %d out of %d filename: %s" % (counter, total_count, row)
    name = row.split('/')[-1].split(".")[0]
    op_file_name = "/home/stonex/Pictures/"+name+"_BICUBIC_output.jpg"
    im = Image.open(row)
    img = im.resize(size, Image.BICUBIC) #  ANTIALIAS)
    img.save(op_file_name)

    # import ipdb
    # ipdb.set_trace()
    counter += 1


# image_file_path = '/home/stonex/Pictures/cat_Dog.png'
# name = image_file_path.split('/')[-1].split(".")[0]

# op_file_name = "/home/stonex/Pictures/"+name+"BICUBIC_output.jpg"


# im = Image.open(image_file_path)
# img = im.resize(size, Image.BICUBIC) #  ANTIALIAS)
#
# img.save(op_file_name)