import numpy as np
import cv2
import pywt
import glob
import os
from matplotlib import pyplot as plt

# tweak this parameter after loading module if reqd
IMAGE_SIZE = (150, 150)

# loads image from folder
def load_dataset(path = '.', preprocess = None, gray = False):
    # load list of classes based
    # on subfolder listing
    class_labels = []
    glob_selector = os.path.join(path, '*')
    print(glob_selector)
    for folder_path in glob.glob(glob_selector):
        class_label = folder_path.split('/')[-1]
        print('Found class label "%s"' % class_label)
        class_labels.append(class_label)
    print(class_labels, len(class_labels))

    # list of image paths
    selected_images = {}
    for class_label in class_labels:
        glob_selector = os.path.join(path, class_label, "*.p*") # select png and ppm
        image_paths = glob.glob(glob_selector)
        print('%d images available for "%s"' % (len(image_paths), class_label))
        selected_images[class_label] = image_paths
    
    # number of images
    n = sum([
        len(selected_images[label]) for label in selected_images
    ])
    print('Selected dataset consisting of', n, 'sample images across classes', class_labels)

    shape = [n, IMAGE_SIZE[0], IMAGE_SIZE[1]]
    shape.append(3) if not gray else None
    images = np.zeros(shape, dtype = 'uint8')
    targets = np.zeros((n, ))

    # load images
    ctr = 0
    target_val = 0
    for class_label in selected_images:
        print('starting read operation for "%s"' % class_label)
        image_paths = selected_images[class_label]
        for image_path in image_paths:
            if gray:
                img = cv2.imread(image_path, 0)
            else: 
                img = cv2.imread(image_path)
            img = cv2.resize(img, IMAGE_SIZE)
            if preprocess:
                assert hasattr(preprocess, '__call__'), 'preprocess is not a function'
                img  = preprocess(img)
            images[ctr] = img
            targets[ctr] = target_val
            ctr += 1
        target_val += 1
        print('done with "%s"' % class_label)

    return images, targets, class_labels  # X, y, labels 

def cv2_imshow(title, image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image)
    else:
        plt.imshow(image, cmap = 'gray')
    plt.title(title)
    plt.axis("off")
    # please use plt.show() as per requirement
