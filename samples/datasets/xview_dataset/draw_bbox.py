import json
from PIL import Image, ImageDraw


coco = json.load(open('./json/training_coco.json'))
# print('[INFO] Coco Images: {}'.format(coco.get('images')))
for image in coco.get('images'):
    annotations = list(filter(lambda elm:elm.get('image_id') == image.get('id'), coco.get('annotations')))
    try:
        im = Image.open('./xview.jpg/train/{}'.format(image.get('file_name')))
    except:
        continue
    draw = ImageDraw.Draw(im)
    for annotation in annotations:
        # draw.rectangle(annotation.get('bbox'))
        for segmentation in annotation.get('segmentation'):
            print('[INFO] Drawing seg: {}'.format(segmentation))
            draw.polygon(segmentation, fill=255)
            

    del draw
    im._planar_configuration = 1
    im.save('./annotated/{}'.format(image.get('file_name')))