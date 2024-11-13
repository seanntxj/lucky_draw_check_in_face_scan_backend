import threading
import time

import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

face_match = False 
reference_img = cv2.imread("img.jpg")

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

while True: 
    ret, frame = cap.read()

    time.sleep(2)
    if ret: 
        try:
            threading.Thread(target=check_face, args=(frame.copy(), )).start()
        except ValueError:
            pass

        if face_match:
            cv2.putText(frame,"Face Found", (50,470),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,255),3)
        else:
            cv2.putText(frame,"No Face Found", (50,470),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,255),3)
        
        cv2.imshow("Face Detection", frame)
        

    key = cv2.waitKey(1)
    if key == ord('q'):
        break 


cv2.destroyAllWindows()