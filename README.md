# Object Detection Experiments
This contains all python code for each dataset on different models

## UNT_Dataset
This contain 2 code files:

These files have to be in the same folder of UNT_dataset:

|--Annotations/
|   |--uav_000001/
|   |...
|--Images/
|   |--uav_000001/
|   |...
|--train_test_split.py
|--yolo_label.py
|--UNT.names

1. train_test_split.py
`python3 train_test_split.py`
To seperate the dataset into 5 subsets (1000 images each) for cross validation

2. yolo_label.py
`python3 yolo_label.py`
To create label files for yolov3

3. UNT.names
Contains names of all classes in the dataset


