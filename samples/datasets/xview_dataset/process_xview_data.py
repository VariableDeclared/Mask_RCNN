import os
import json
from PIL import Image

data = json.load(open('xView_train.geojson'))
print("[INFO] Loaded xview json.")

seen = {}
new_dict = {}
new_data = {
    'features': []
}
not_processed = []
for feature in data['features']:
    img_name = feature.get('properties').get('image_id')
    path = './train_images/{}'.format(img_name)


    if not os.path.exists(path):
        path = './val_images/{}'.format(img_name)


    if not os.path.exists(path):
        print('[INFO] Could not find: {}'.format(path))
        not_processed.append(path)
        continue

    if seen.get(img_name) is not None:
        print("[INFO] Already processed: {}".format(img_name))
        feature['properties'].update(seen.get(img_name).get('dims'))
        # feature['geometry']['coordinates'] = seen.get(img_name).get('coords')
        continue
    
    
    seen[img_name] = {}
    print('[INFO] processing: {}'.format(path))
    with Image.open('./train_images/{}'.format(img_name)) as im:
        width, height = im.size
        dimensions = {
            "img_width": width,
            "img_height": height
        }
        feature['properties'].update(dimensions)
        seen[img_name]['dims'] = dimensions

    



# data.update(new_data)


new_fh = open('xview_data.new.json', 'w')
not_proc_fh = open('not_processed.json', 'w')
json.dump(not_processed, not_proc_fh)
json.dump(data, new_fh)

new_fh.close()
not_proc_fh.close()

print('[INFO] Dumped json to xview_data.new.json')