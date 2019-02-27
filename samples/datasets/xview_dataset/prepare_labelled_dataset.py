import json
import os
import copy

print("[INFO] COCO PROCESSOR, MADE TO PROCESS ALL THE COCOZ")

JSON_FILE_NAME = "xview_custom_labels_coco.json" # input("Enter the file to get the coco from?? mmmmm Coco... \n")
labelled_coco = json.load(open(JSON_FILE_NAME))

def filter_annotations(img_id, annotation_set):
    return list(filter(lambda elm:elm.get('image_id') != img_id, annotation_set))

new_image_payload = []
for image in labelled_coco.get('images'):
    image.update({
        'file_name': image.get('file_name').split('-')[-1]
    })
    new_image_payload.append(image)


print("[INFO] Trimming Annotations, Annotation classes: {}".format(list(map(lambda elm:elm.get('name'), labelled_coco.get('categories')))))

exclude_classes = input("\n").split(",")


labelled_coco['categories'] = list(filter(lambda elm: elm.get('name') not in exclude_classes, labelled_coco.get('categories')))
cat_ids = list(map(lambda elm: elm.get('id'), labelled_coco.get('categories')))
print("[INFO] Chosen classes: {}, IDs: {}".format(list(map(lambda elm: elm.get('name'), labelled_coco.get('categories'))), cat_ids))
print("[DEBUG] Anno len: {}".format(len(labelled_coco.get('annotations'))))
labelled_coco['annotations'] = list(filter(lambda elm: elm.get('category_id') in cat_ids, labelled_coco.get('annotations')))
print("[DEBUG] Anno len: {}".format(len(labelled_coco.get('annotations'))))
### Create training (20/30 - main -> rest for validation 10/20)

# training_images = copy.deepcopy(labelled_coco)
images = labelled_coco.get('images')

num_train = eval(input("How many images do you want in the training set? {} Images total \n".format(len(images))))

# Adjust accordingly
training_images = [img.get('id') for img in images[0:num_train]]
validation_images = [ img.get('id') for img in images[num_train:]]

training_images_coco = copy.deepcopy(labelled_coco)
validation_images_coco = copy.deepcopy(labelled_coco)
training_images_coco['images'] = []
validation_images_coco['images'] = []
training_images_coco['annotations'] = []
validation_images_coco['annotations'] = []

annotations = labelled_coco.get('annotations')
val_img = []
train_img = []
for image in images:
    img_id = image.get('id')
    
    if img_id in training_images:
        train_img.append(image)
        training_images_coco['annotations'].extend(
            filter_annotations(img_id, annotations)
        )
    if img_id in validation_images:
        val_img.append(image)
        validation_images_coco['annotations'].extend(
            filter_annotations(img_id, annotations)
        )
    

training_images_coco['images'] = train_img
validation_images_coco['images'] = val_img

print("[INFO] Classes: {}".format(len(labelled_coco.get('categories'))))
train_fh = open('./json/training_coco.json', 'w')
val_fh = open('./json/val_coco.json', 'w')

json.dump(training_images_coco, train_fh)
json.dump(validation_images_coco, val_fh)

train_fh.close()
val_fh.close()