import time
import cv2
import os

def start(q, data_dir = '.', limit = 30, time_gap = 2):
    print('start saving face images')
    ctr = 0
    switch = True
    while switch and (ctr < limit):
        switch, faces = q.get()
        for face in faces:
            image_path = os.path.join(data_dir, str(ctr) + '.png')
            cv2.imwrite(image_path, face)
            ctr += 1
            time.sleep(time_gap)
        print('saved', ctr, 'faces', end = '\r')
    print('save process finished. press q')