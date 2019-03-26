"""
Split these 5000 images into two parts, train(4500) and test(500).

Steps:
    1. Rename every image and annotation: `folder_name + 000000.jpg`;
    2. Put all images and annotations into one folder separately;
    3. Select 500 images randomly to create sud-dataset for test;

    ./data/
        |-> train/
            \-> Images/
            |-> Annotations/
        |-> test/
            |-> Images/
            |-> Annotations

    Finally rename `./data/` to `./UNT_Aerial_Dataset/`, for now I use `./data/`
    in order to different from the parent name.
"""
import os
import shutil
import numpy as np
from numpy import random as rd

ROOT_DIR = './'
DATA_DIR = 'data/'
IMAGES = 'Images/'
ANNOTATIONS = 'Annotations/'


def copy_rename(old_dir, folder_name, new_folder):
    dir = os.path.join(old_dir, folder_name)
    files = sorted(os.listdir(dir))
    new_dir = os.path.join(DATA_DIR, new_folder)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for file in files:
        old_file = os.path.join(dir, file)
        new_file = os.path.join(new_dir, folder_name + '_' + file)
        shutil.copy(old_file, new_file)


def split_train_test():
    test_index = rd.choice(5000, 500, replace=False)
    test_dir = os.path.join(DATA_DIR, 'test')
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
        os.mkdir(test_dir + '/Images')
        os.mkdir(test_dir + '/Annotations')
    # Move images and annotations
    images = sorted(os.listdir(DATA_DIR + IMAGES))
    annotations = sorted(os.listdir(DATA_DIR + ANNOTATIONS))
    for i in test_index:
        old_image = os.path.join(DATA_DIR, IMAGES, images[i])
        new_image = os.path.join(DATA_DIR, 'test', IMAGES, images[i])
        shutil.move(old_image, new_image)
        
        old_annotation = os.path.join(DATA_DIR, ANNOTATIONS, annotations[i])
        new_annotation = os.path.join(DATA_DIR, 'test', ANNOTATIONS, annotations[i])
        shutil.move(old_annotation, new_annotation)

#slip the data into 5 subsets randomly
def split_subset():
    shuffle_index = rd.choice(5000, 5000, replace=False)
    sub_indexes = np.array_split(shuffle_index, 5)
    subset_dirs = [os.path.join(DATA_DIR, 'subset%s'%i) for i in range(1,6)]
    images = sorted(os.listdir(DATA_DIR + IMAGES))
    annotations = sorted(os.listdir(DATA_DIR + ANNOTATIONS))
    for sub_index, sub_dir in zip(sub_indexes, subset_dirs):
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
            os.mkdir(sub_dir + '/Images')
            os.mkdir(sub_dir + '/Annotations')
        for i in sub_index:
            old_image = os.path.join(DATA_DIR, IMAGES, images[i])
            new_image = os.path.join(sub_dir, IMAGES, images[i])
            shutil.move(old_image, new_image)
            old_annotation = os.path.join(DATA_DIR, ANNOTATIONS, annotations[i])
            new_annotation = os.path.join(sub_dir, ANNOTATIONS, annotations[i])
            shutil.move(old_annotation, new_annotation)
        print(len(os.listdir(sub_dir + '/' + IMAGES)))

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.mkdir(ROOT_DIR + DATA_DIR)
        image_folders = sorted(os.listdir(IMAGES))
        annotation_folders = sorted(os.listdir(ANNOTATIONS))
        for image_folder in image_folders:
            copy_rename(IMAGES, image_folder, IMAGES)
        for annotation_folder in annotation_folders:
            copy_rename(ANNOTATIONS, annotation_folder, ANNOTATIONS)
    split_subset()
