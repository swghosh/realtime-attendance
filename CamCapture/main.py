import camera
import facesave

from multiprocessing import Process
from multiprocessing import Queue

import os

DATA_DIR = '/Volumes/Card/Datasets/RA-Data/another-dataset'
TIME_GAP = 1 # in seconds

def main():
    name = input('Your name? ')
    folder_path = os.path.join(DATA_DIR, name)
    os.mkdir(folder_path)
    limit = int(input('Number of images? '))

    q = Queue(maxsize = 1)
    cam = Process(target = camera.start, args = (q,))
    save = Process(target = facesave.start, args = (q, folder_path, limit, TIME_GAP))
    cam.start()
    save.start()
    cam.join()
    save.join()

if __name__ == '__main__':
    main()