import numpy as np
from PIL import Image
import os

mode = input("Enter mode")
files = [f for f in os.listdir('./{}'.format(mode)) if os.path.isfile(os.path.join('./{}'.format(mode), f))]

xDims, yDims = [], []
for image_file in files:
    with Image.open('./{}/{}'.format(mode, image_file)) as im:
        width, height = im.size

        xDims.append(width)
        yDims.append(height)


print("Max width: {}, max height: {}".format(np.max(xDims), np.max(yDims)))
print("Min width: {}, min height: {}".format(np.min(xDims), np.min(yDims)))

