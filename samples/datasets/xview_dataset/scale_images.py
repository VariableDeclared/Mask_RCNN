import PIL
from PIL import Image
from os import listdir
from os.path import isfile, join



for dir in ['./train_images', './val_iamges']:
    for file in [f for f in listdir(dir) if isfile(join(dir, f))]:
        img = Image.open("{}/{}".format(dir, file))
        maxsize = (512, 512)
        img.thumbnail(maxsize, Image.ANTIALIAS)
        scaled = img.copy()
        scaled.save("{}/scaled/{}".format(dir, file))



print('[INFO] DONE.')