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

    if len(imgs) < 30 or imgs.get(img_name):
        # print("[INFO] Processing: {}".format(img_name))
        
        new_data['annotations'].append({
            "segmentation": [scaled_coords],
            "iscrowd": 0,
            "image_id": imgs[img_name][0],
            "category_id": feature.get('properties').get('type_id'),
            "id": i,
            "bbox": scaled_coords,
            "area": 0
        })
        
    i += 1

for img in imgs:
    new_data['images'].append({
            "license": 0,
			"file_name": img,
			"width": 512,
			"height": 512,
			"id": imgs[img][0]
    })


new_data["categories"] = [{"supercategory": "resources", "id": 11, "name": "Fixed-wing Aircraft "}, {"supercategory": "resources", "id": 12, "name": "Small Aircraft "}, {"supercategory": "resources", "id": 13, "name": "Passenger/Cargo Plane "}, {"supercategory": "resources", "id": 15, "name": "Helicopter "}, {"supercategory": "resources", "id": 17, "name": "Passenger Vehicle "}, {"supercategory": "resources", "id": 18, "name": "Small Car "}, {"supercategory": "resources", "id": 19, "name": "Bus "}, {"supercategory": "resources", "id": 20, "name": "Pickup Truck "}, {"supercategory": "resources", "id": 21, "name": "Utility Truck "}, {"supercategory": "resources", "id": 23, "name": "Truck "}, {"supercategory": "resources", "id": 24, "name": "Cargo Truck "}, {"supercategory": "resources", "id": 25, "name": "Truck Tractor w/ Box Trailer "}, {"supercategory": "resources", "id": 26, "name": "Truck Tractor "}, {"supercategory": "resources", "id": 27, "name": "Trailer "}, {"supercategory": "resources", "id": 28, "name": "Truck Tractor w/ Flatbed Trailer "}, {"supercategory": "resources", "id": 29, "name": "Truck Tractor w/ Liquid Tank "}, {"supercategory": "resources", "id": 32, "name": "Crane Truck "}, {"supercategory": "resources", "id": 33, "name": "Railway Vehicle "}, {"supercategory": "resources", "id": 34, "name": "Passenger Car "}, {"supercategory": "resources", "id": 35, "name": "Cargo/Container Car "}, {"supercategory": "resources", "id": 36, "name": "Flat Car "}, {"supercategory": "resources", "id": 37, "name": "Tank car "}, {"supercategory": "resources", "id": 38, "name": "Locomotive "}, {"supercategory": "resources", "id": 40, "name": "Maritime Vessel "}, {"supercategory": "resources", "id": 41, "name": "Motorboat "}, {"supercategory": "resources", "id": 42, "name": "Sailboat "}, {"supercategory": "resources", "id": 44, "name": "Tugboat "}, {"supercategory": "resources", "id": 45, "name": "Barge "}, {"supercategory": "resources", "id": 47, "name": "Fishing Vessel "}, {"supercategory": "resources", "id": 49, "name": "Ferry "}, {"supercategory": "resources", "id": 50, "name": "Yacht "}, {"supercategory": "resources", "id": 51, "name": "Container Ship "}, {"supercategory": "resources", "id": 52, "name": "Oil Tanker "}, {"supercategory": "resources", "id": 53, "name": "Engineering Vehicle "}, {"supercategory": "resources", "id": 54, "name": "Tower crane "}, {"supercategory": "resources", "id": 55, "name": "Container Crane "}, {"supercategory": "resources", "id": 56, "name": "Reach Stacker "}, {"supercategory": "resources", "id": 57, "name": "Straddle Carrier "}, {"supercategory": "resources", "id": 59, "name": "Mobile Crane "}, {"supercategory": "resources", "id": 60, "name": "Dump Truck "}, {"supercategory": "resources", "id": 61, "name": "Haul Truck "}, {"supercategory": "resources", "id": 62, "name": "Scraper/Tractor "}, {"supercategory": "resources", "id": 63, "name": "Front loader/Bulldozer "}, {"supercategory": "resources", "id": 64, "name": "Excavator "}, {"supercategory": "resources", "id": 65, "name": "Cement Mixer "}, {"supercategory": "resources", "id": 66, "name": "Ground Grader "}, {"supercategory": "resources", "id": 71, "name": "Hut/Tent "}, {"supercategory": "resources", "id": 72, "name": "Shed "}, {"supercategory": "resources", "id": 73, "name": "Building "}, {"supercategory": "resources", "id": 74, "name": "Aircraft Hangar "}, {"supercategory": "resources", "id": 76, "name": "Damaged Building "}, {"supercategory": "resources", "id": 77, "name": "Facility "}, {"supercategory": "resources", "id": 79, "name": "Construction Site "}, {"supercategory": "resources", "id": 83, "name": "Vehicle Lot "}, {"supercategory": "resources", "id": 84, "name": "Helipad "}, {"supercategory": "resources", "id": 86, "name": "Storage Tank "}, {"supercategory": "resources", "id": 89, "name": "Shipping container lot "}, {"supercategory": "resources", "id": 91, "name": "Shipping Container "}, {"supercategory": "resources", "id": 93, "name": "Pylon "}, {"supercategory": "resources", "id": 94, "name": "Tower"}]
new_fh = open('xview_coco.{}.json'.format(mode_input), 'w')
not_proc_fh = open('not_processed.json', 'w')
json.dump(not_processed, not_proc_fh)
json.dump(new_data, new_fh)

new_fh.close()
not_proc_fh.close()

print('[INFO] Dumped json to xview_data.{}.json'.format(mode_input))