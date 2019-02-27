from PIL import Image
import os


mode = input("Enter mode")

files = [f for f in os.listdir('./{}'.format(mode)) if os.path.isfile(os.path.join('./{}'.format(mode), f))]

for image_name in files:
    im = Image.open('./{}/{}'.format(mode, image_name))
    
    im.thumbnail((512, 512), Image.ANTIALIAS)

    im.save('./{}/scaled/{}'.format(mode, image_name))
    print('[INFO] Scaled {}'.format(image_name))