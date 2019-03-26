#!/usr/bin/env python
# coding: utf-8

# This is to getting the output from yolov3 result.classname.txt files and comparing with the truth label to calculating the AP score for each class and the mAP of the dataset.

# In[1]:


import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pickle
import numpy as np
import os
from os import listdir, getcwd
from os.path import join

PATH='./data/'
ANNO='Annotations/'
IMG='Images/'
NAMES=["person", "boat", "car", "bicycle", "truck", "bus"]


# In[2]:


#A, B: (xm, ym, xM, yM)
def IoU (A, B):
    I = [max(A[0], B[0]),  #xm of Intersect
        max(A[1], B[1]),   #ym
        min(A[2], B[2]),   #xM
        min(A[3], B[3])]   #yM
    return area(I) / (area(A) + area(B) - area(I))

#box: (xm, ym, xM, yM)
def area (box):
    return max(0, (box[2]-box[0])) * max(0, (box[3]-box[1]))

#testfolder is the directory_name of the subset used for testing
#eg. 'subset1/' Must include '/'
#get the total numbers of all objects in the particular testing subfolder
def get_Number_of_Objects(testfolder):
    numberOfObjects = [0, 0, 0, 0, 0, 0]
    path = PATH+testfolder+ANNO
    listOfAllAnnotations = os.listdir(path)
    for file in listOfAllAnnotations:
        in_file = open(path+file)
        tree=ET.parse(in_file)
        root = tree.getroot()
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            name = obj.find('name').text
            if int(difficult) == 1:
                continue
            try:
                numberOfObjects[NAMES.index(name)] += 1
            except:
                print (name)
                print (path+file)
    return numberOfObjects

#xm, ym, xM, yM
#label = ["uav_000001_000003", 0.991271, 588.334778, 238.953278, 658.364563, 310.355133]
#get y_true value
def is_correct_name(testfolder, label, class_name, thres = 0.5):
    path = PATH+testfolder+ANNO
    in_file = open('%s%s.xml'%(path+label[0]))
    tree=ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        name = obj.find('name').text
        if name != class_name or int(difficult) == 1:
            continue
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text))
        if IoU(b, label[2:].astype(float)) < thres:
            continue
        else:
            return 1
    return 0

#to smoothen the curve by recall & precision, only used in average_precision_score
#recall, precision: np.ndarray
def smoothening (recall, precision):
    size = len(recall)*1000
    recall = np.append(recall, 1.0)
    precision = np.append(precision, 0.0)
    newRecall = np.array([index/size for index in range (size, -1, -1)])
    newPrecision = np.array([precision[np.searchsorted(recall, r)] for r in newRecall])
    return newRecall, newPrecision

#calculate AP score for each class
#y_true: 1 if correct label based on IoU, 0 otherwise
#y_score: confident level of the bounding box range [0, 1]
#totalTruthBB: the total number of ground truth boxes for the class in the dataset, 
#leave None if assuming the model finds all of the ground truth boxes
def my_average_precision_score (y_true, y_score, totalTruthBB = None):
    size = len(y_true)
    if size == len(y_score):
        y_true = y_true[np.argsort(-y_score)]
        numberTruthLabels = sum(y_true) if totalTruthBB == None else totalTruthBB
        correctLabels = np.array([sum(y_true[:index]) for index in range (1, size+1)])
        recall = correctLabels/numberTruthLabels
        precision = correctLabels/np.arange(1, size+1)
        newRecall, newPrecision = smoothening(recall, precision)
        #this part to show the graph, comment it for faster speed
        plt.plot(recall, precision, 'r-')
        plt.plot(newRecall, newPrecision, 'b-')
        plt.axis([0, 1, 0, 1])
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.fill_between(recall, precision, facecolor='red', alpha=0.1)
        plt.fill_between(newRecall, newPrecision, facecolor='blue', alpha=0.1)
        plt.show()
        return sum(newPrecision)/len(newPrecision)
    
# In[3]:

mAPScore = 0.0
numberOfAllObjects = get_Number_of_Objects('subset1/')
for name, numberOfObject in zip(NAMES, numberOfAllObjects):
    with open('comp4_det_test_%s.txt'%name) as f:
        lines = np.array([line.strip("\n").split(" ") for line in f])
    y_score = np.array([float(line[1]) for line in lines])
    y_true = np.array([is_correct_name('subset1/', line, name, 0.5) for line in lines])
    APScore = my_average_precision_score(y_true, y_score, numberOfObject)
    print ("Number of BBs found by yolov3 for class %s is %s."%(name, sum(y_true)))
    print ('Average Precision score is %s'%APScore)
    mAPScore += APScore
mAPScore /= len(NAMES)
print ('mAP score of this dataset is %s'%mAPScore)
