import os
import shutil
import random

train_split = 0.8
validation_split = 0.2
test_split = 0.0

if (round(train_split + validation_split + test_split, 5) != 1.0):
    raise Exception('Error: values do not add to 1')



# Creating train, validation, test // deleting previous partitions containing old data
root = 'grids'
for path in (f'{root}/images', f'{root}/labels'):

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)
    os.mkdir(f'{path}/test')
    os.mkdir(f'{path}/train')
    os.mkdir(f'{path}/validation')


# Storing a list of all images and their labels
items_list = []
for _, _, files in os.walk(f'{root}/images_uncategorised'):
    for file in files:
        name = file.split('.')[0]

        items_list.append(name)

random.shuffle(items_list)

# Moving images into specified categories

for i, name in enumerate(items_list):

    image_filepath = f'{root}/images_uncategorised/{name}.jpg'
    label_filepath = f'{root}/labels_uncategorised/{name}.txt'

    category = ''

    if i / len(items_list) <= train_split:
        category = 'train'
    elif i / len(items_list) <= train_split + validation_split:
        category = 'validation'
    else:
        category = 'test'

        
    categorised_image = f'{root}/images/{category}/{name}.jpg'
    categorised_label = f'{root}/labels/{category}/{name}.txt'

    shutil.copy(image_filepath, categorised_image)
    shutil.copy(label_filepath, categorised_label)

   


