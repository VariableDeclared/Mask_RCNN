import os
import os.path
import json
from PIL import Image

data = json.load(open('./xview_dataset/xView_train.geojson'))
print("[INFO] Loaded xview json.")

seen = {}
new_dict = {}
new_data = {
    "images": [],
    "annotations": [],
    "categories": []
}
not_processed = []
files = [f for f in os.listdir('./val') if os.path.isfile(os.path.join('./val', f))]
seen = {}
i = 0
images = []
for feature in data['features']:
    """ Process into coco-like dataset """
    img_name = feature.get('properties').get('image_id')

    

    if img_name not in files:
        print("[INFO] Skipping {}".format(img_name))
        if img_name not in not_processed:
            not_processed.append(img_name)
        continue
    
    
    coords = feature.get('properties').get('bounds_imcoords')
    coords_sets = []
    for coordset in coords:
        new_set = []
        for coord in coordset:
            new_set = new_set + coord
        coords_sets.append(new_set)
    
    if seen.get(img_name) is None:
        images.append(img_name)

    seen[img_name] = True
    
    if len(seen) < 30 or seen.get(img_name):
        print("[INFO] Processing: {}".format(img_name))
        
        new_data['annotations'].append({
            "segmentation": coords_sets,
            "iscrowd": 0,
            "image_id": img_name,
            "category_id": feature.get('properties').get('type_id'),
            "id": i,
            "bbox": feature.get('properties').get('bounds_imcoords').split(','),
            "area": 0
        })
    i += 1

for img in images:
    new_data['images'].append({
            "license": 0,
			"file_name": img,
			"width": 512,
			"height": 512,
			"id": i
    })
    i += 1
i = 0
        



new_fh = open('xview_coco.val.json', 'w')
not_proc_fh = open('not_processed.json', 'w')
json.dump(not_processed, not_proc_fh)
json.dump(new_data, new_fh)

new_fh.close()
not_proc_fh.close()

print('[INFO] Dumped json to xview_data.new.json')