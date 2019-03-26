import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=['subset1', 'subset2', 'subset3', 'subset4', 'subset5']

classes = ["person", "boat", "car", "bicycle", "truck", "bus"]

DATA = 'data/'


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_set, image_id):
    in_file = open('data/%s/Annotations/%s.xml'%(image_set, image_id))
    out_file = open('data/%s/Images/%s.txt'%(image_set, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for image_set in sets:
    #image_ids = open('data/%s.txt'%(image_set)).read().strip().split()
    image_ids = os.listdir('%s%s/Images'%(DATA, image_set))
    list_file = open('%s%s.txt'%(DATA, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/%s%s/Images/%s\n'%(wd, DATA, image_set, image_id))
        convert_annotation(image_set, image_id[:-4])
    list_file.close()
