'''
Demo script to showcase the use of DeepFace to detect and recognize faces. 
Run opencam.py first before attempting this to ensure opencv can access your webcam properly.
'''

import time
import cv2
from deepface import DeepFace
import threading 
from pathlib import Path
from src.face_api import check_face

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# reference_img = cv2.imread("img.jpg")
person_found = False

def check_face_aux(frame):
	global person_found

	list_of_potential_persons = check_face(frame)
	print(list_of_potential_persons)
	if len(list_of_potential_persons) > 0:
		person_found = list_of_potential_persons[0]  
	else:
		person_found = 'Unknown person'
	
count = 50
while True:
	ret, frame = cap.read()
	time.sleep(0.1)
	count -= 1
	if ret and count == 0:
		count = 10
		try: 
			t = threading.Thread(target=check_face_aux, args=(frame.copy(),), )
			t.start()
			t.join()
		except ValueError: 
			pass
		finally: 
			pass
	
	if person_found:
		cv2.putText(frame, person_found, (50, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
	else:
		cv2.putText(frame, "No Face Found", (50, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

	cv2.imshow("Face Detection", frame)

	key = cv2.waitKey(1)
	if key == ord('q'):
		break

cv2.destroyAllWindows()