import cv2
import glob 



def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    
    dataset = []
    
    
    filelist = glob.glob(str(dataPath)+"/face/*.pgm")
    for file_name in filelist:
        new_element = (cv2.imread(file_name, cv2.IMREAD_GRAYSCALE), 1)
        dataset.append(new_element)


    filelist = glob.glob(str(dataPath)+"/non-face/*.pgm")
    for file_name in filelist:
        new_element = (cv2.imread(file_name, cv2.IMREAD_GRAYSCALE), 0)
        dataset.append(new_element)


    #raise NotImplementedError("To be implemented")
    
    # End your code (Part 1)
    return dataset
