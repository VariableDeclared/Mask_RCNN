import os
import os.path
import json
from PIL import Image

data = json.load(open('./xview_dataset/xView_train.geojson'))
print("[INFO] Loaded xview json.")

seen = {}
new_dict = {}
new_data = {
    'features': []
}
not_processed = []
files = [f for f in os.listdir('./xview_dataset/train_images/scaled') if os.path.isfile(os.path.join('./xview_dataset/train_images/scaled', f))]
for feature in data['features']:
    img_name = feature.get('properties').get('image_id')
    path = './xview_dataset/train_images/scaled/{}'.format(img_name)



    if not os.path.exists(path) or img_name not in files[31:61]:
        print('[INFO] Skipping: {}'.format(path))
        not_processed.append(path)
        continue

    if seen.get(img_name) is not None:
        print("[INFO] Already processed: {}".format(img_name))
        feature['properties'].update(seen.get(img_name).get('dims'))
        # feature['geometry']['coordinates'] = seen.get(img_name).get('coords')
        continue
    
    
    seen[img_name] = {}
    print('[INFO] processing: {}'.format(path))
    with Image.open('./xview_dataset/train_images/scaled/{}'.format(img_name)) as im:
        width, height = im.size
        dimensions = {
            "img_width": 512,
            "img_height": 512
        }
        feature['properties'].update(dimensions)
        seen[img_name]['dims'] = dimensions
    new_data['features'].append(feature)


data['features'] = new_data['features']


new_fh = open('xview_data.val.json', 'w')
not_proc_fh = open('not_processed.json', 'w')
json.dump(not_processed, not_proc_fh)
json.dump(data, new_fh)

new_fh.close()
not_proc_fh.close()

print('[INFO] Dumped json to xview_data.new.json')