import os
import json

contents = None

with open('xView_train.geojson', 'r') as f:
    contents = f.read()
    if contents is None:
        print("[ERROR] Contents is None")
        exit(1)

print("[INFO] Got contents.")

content_dict = json.loads(contents)

print("[INFO] Loaded Contents!")

print("[INFO] Keys: {}".format(content_dict.keys()))

