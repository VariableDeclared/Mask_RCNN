import json
import numpy as np

def get_labels(fname="xView_train.geojson"):
    with open(fname) as f:
        data = json.load(f)
    
    coords = np.zeros((len(data['features']),4))
    chips = np.zeros((len(data['features'])),dtype="object")
    classes = np.zeros((len(data['features'])))
    for i in range(len(data['features'])):
        if data['features'][i]['properties']['bounds_imcoords'] != []:
            b_id = data['features'][i]['properties']['image_id']
            val = np.array([int(num) for num in data['features'][i]['properties']['bounds_imcoords'].split(",")])
            chips[i] = b_id
            classes[i] = data['features'][i]['properties']['type_id']
            coords[i] = val
        else:
            chips[i] = 'None'
    return coords, chips, classes

print(get_labels("D:\\computer_vision_labs\\Mask_RCNN\\samples\\datasets\\xview_dataset\\json\\xView_train.geojson"))