import os
import os.path
import json
from PIL import Image


def get_width_and_height(file):
    width, height = (0, 0)
    with Image.open(file) as im:
        width, height = im.size
    
    return width, height

data = json.load(open('./json/xView_train.geojson'))
class_ids_json = json.load(open('./json/class_ids.edited.json'))

print("[INFO] Loaded xview json.")


new_dict = {}
new_data = {
    "images": [],
    "annotations": [],
    "categories": []
}
not_processed = []
mode = ['val', 'train']
mode_input = input("Enter mode \n")

if mode_input not in mode: 
    print("Mode not valid, use val or train")
    exit(1)

files = [f for f in os.listdir('./{}/scaled'.format(mode_input)) if os.path.isfile(os.path.join('./{}/scaled'.format(mode_input), f))]
class_ids = [class_id.get('id') for class_id in class_ids_json]

imgs = {}
i = 0

for feature in data['features']:
    """ Process into coco-like dataset """
    img_name = feature.get('properties').get('image_id')

    

    if img_name not in files:
        # print("[INFO] Skipping {}".format(img_name))
        if img_name not in not_processed:
            not_processed.append(img_name)
        continue
    
    
    coords = feature.get('properties').get('bounds_imcoords').split(',')
    details = imgs.get(img_name)
    imgwidth = 0
    imgheight = 0
    if details is not None:
        imgwidth = details[1]
        imgheight = details[2]
    else:
        imgwidth, imgheight = get_width_and_height("./{}/{}".format(mode_input, img_name))
        print("[INFO]: Got height and width from {}, W: {} H: {}".format("./{}/{}".format(mode_input, img_name), imgwidth, imgheight))
        imgs[img_name] = [i, imgwidth, imgheight]


    xScale = 512 / imgwidth
    yScale = 512 / imgheight
    print("[INFO] Scaling by x: {} y: {}".format(xScale, yScale))
    scaled_coords = [int(coords[0])*xScale, int(coords[1])*yScale, int(coords[2])*xScale, int(coords[3])*yScale]
    class_id = feature.get('properties').get('type_id')

    # Check we want this class annotatation AND that we have <= 30 images, if
    # over 30 but the image is one we already have, add annotation.
    if class_id in class_ids and (len(imgs) < 30 or imgs.get(img_name)):
        # print("[INFO] Processing: {}".format(img_name))
        # Only add image if it has an annotation.
        if details is not None:
            imgwidth = details[1]
            imgheight = details[2]
        else:
            imgwidth, imgheight = get_width_and_height("./{}/{}".format(mode_input, img_name))
            print("[INFO]: Got height and width from {}, W: {} H: {}".format("./{}/{}".format(mode_input, img_name), imgwidth, imgheight))
            imgs[img_name] = [i, imgwidth, imgheight]

        new_data['annotations'].append({
            "segmentation": [scaled_coords],
            "iscrowd": 0,
            "image_id": imgs[img_name][0],
            "category_id": class_id,
            "id": i,
            "bbox": scaled_coords,
            "area": 0
        })
        
    i += 1

for img in imgs:
    details = imgs.get(img)
    new_data['images'].append({
            "license": 0,
			"file_name": img,
			"width": details[1],
			"height": details[2],
			"id": details[0]
    })


new_data["categories"] = class_ids_json
new_fh = open('./json/xview_coco.{}.json'.format(mode_input), 'w')
not_proc_fh = open('not_processed.json', 'w')
json.dump(not_processed, not_proc_fh)
json.dump(new_data, new_fh)

new_fh.close()
not_proc_fh.close()
print('[INFO] NUMBER OF CLASSES IN THIS BATCH: {}'.format(len(class_ids)))
print('[INFO] Dumped json to xview_data.{}.json'.format(mode_input))