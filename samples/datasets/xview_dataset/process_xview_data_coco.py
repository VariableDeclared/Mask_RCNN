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

files = [f for f in os.listdir('./{}'.format(mode_input)) if os.path.isfile(os.path.join('./{}'.format(mode_input), f))]
class_ids = [class_id.get('id') for class_id in class_ids_json]
print('[DEBUG] Class IDS: {}'.format(class_ids))

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
    coords = list(map(int, coords))
    class_id = feature.get('properties').get('type_id')
 
    # Check we want this class annotatation AND that we have <= 30 images, if
    # over 30 but the image is one we already have, add annotation.
    if class_id in class_ids and (len(imgs) < 30 or imgs.get(img_name)):
        # Only add image if it has an annotation.
        if details is not None:
            imgwidth = details[1]
            imgheight = details[2]
        else:
            imgwidth, imgheight = get_width_and_height("./{}/{}".format(mode_input, img_name))
            print("[INFO]: Got height and width from {}, W: {} H: {}".format("./{}/{}".format(mode_input, img_name), imgwidth, imgheight))
            imgs[img_name] = [i, imgwidth, imgheight]

        # print("[INFO] Processing: {}".format(img_name))
        new_data['annotations'].append({
            "segmentation": [coords],
            "iscrowd": 0,
            "image_id": imgs[img_name][0],
            "category_id": class_id,
            "id": i,
            "bbox": coords,
            "area": 0
        })
    
        # print('[INFO] Class ID: {} not in set'.format(class_id)) 
        
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