import json
from PIL import Image, ImageDraw


coco = json.load(open('xview_coco.train.json'))

for annotation in coco.get('annoatations'):

for image in coco.get('images'):
    annoatations = list(filter(lambda elm:elm.get('image_id') == image.get('id')))
    im = Image.open('./train/{}'.format(image.get('image_name')))
    draw = ImageDraw.Draw(im)
    for annotation in annoatations:
        draw.rectangle(annotation.get('bbox'))

    del draw
    im.save()