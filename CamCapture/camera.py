import cv2
import numpy as np
import os
import time

def start(q):

    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier('../cascades/lbpcascades/lbpcascade_frontalface_improved.xml')

    rect_color = (0, 0, 255) # BGR, not RGB
    rect_stroke = 2

    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame_flipped = cv2.flip(frame, 1)
        gray_flipped = cv2.flip(gray, 1)

        del frame
        del gray

        faces = face_cascade.detectMultiScale(gray_flipped, scaleFactor = 1.2, minNeighbors = 5)
        
        current_faces = []

        for (x, y, w, h) in faces:
            face = gray_flipped[y:y+h, x:x+w]
            current_faces.append(face)

            cv2.rectangle(frame_flipped, (x, y), (x + w, y + h), rect_color, rect_stroke)
        
        if q.full():
            q.get()
        q.put((True, current_faces))

        cv2.imshow('Camera', frame_flipped)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    
    q.put((False, []))

    cap.release()
    cv2.destroyAllWindows()
