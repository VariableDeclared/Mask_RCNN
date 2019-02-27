import os
import os.path
import json
from PIL import Image

FILE_NAME = './xview_coco.val.json'
data = json.load(open(FILE_NAME, 'r'))
print("[INFO] Loaded coco json.")
class_ids = open('./xview_dataset/class_ids.json', 'r')
class_ids_dict = json.load(class_ids)
class_ids.close()

new_data = {
    "images": data.get('images'),
    "annotations": data.get('annotations'),
    "categories": []
}
not_processed = []
files = [f for f in os.listdir('./xview_dataset/train_images/scaled') if os.path.isfile(os.path.join('./xview_dataset/train_images/scaled', f))]

for id in class_ids_dict:
    """ Process into coco-like dataset """
    new_data['categories'].append({
			"supercategory": "resources",
			"id": int(id),
			"name": class_ids_dict[id]
		})



        



json_fh = open('./json/xview_coco.ci.val.json', 'w')
not_proc_fh = open('not_processed.json', 'w')
json.dump(not_processed, not_proc_fh)
json.dump(new_data, json_fh)

json_fh.close()
not_proc_fh.close()

print('[INFO] Dumped json to xview_data.new.json')