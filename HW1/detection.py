import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    f = open(dataPath, "r")
    file_list = []

    for line in f:
        spilt_str = line.split(' ')
        if len(spilt_str) == 2:
            file_list.append((spilt_str[0], []))
        elif len(spilt_str) == 4:
            file_list[-1][1].append((int(spilt_str[0]), int(spilt_str[1]), int(spilt_str[2]), int(spilt_str[3])))
    
    for file in file_list:
        img_original = cv2.imread("data/detect/" + file[0])
        img = cv2.imread("data/detect/" + file[0], cv2.IMREAD_GRAYSCALE)
        for face_area in file[1]:
            face = img[face_area[1]:face_area[1]+face_area[3], face_area[0]:face_area[0]+face_area[2]]
            face = cv2.resize(face, (19, 19), interpolation=cv2.INTER_LINEAR)
            result = clf.classify(face)
            if result == 1:
                cv2.rectangle(img_original, (face_area[0], face_area[1]), (face_area[0] + face_area[2], face_area[1] + face_area[3]), (0, 255, 0), thickness=4)
            else:
                cv2.rectangle(img_original, (face_area[0], face_area[1]), (face_area[0] + face_area[2], face_area[1] + face_area[3]), (0, 0, 255), thickness=4)
        img_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)
        plt.axis('off')
        plt.imshow(img_original)
        plt.show()
    # End your code (Part 4)
