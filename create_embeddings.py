'''
Forces the creation of embeddings for the images in a given folder.
Ensure to run before using face_api.py
'''

from deepface import DeepFace
import numpy as np

FACES_FOLDER_FILE_PATH = 'faces'

blank_image = np.zeros((640, 480, 3), np.uint8)

# Using RetinaFace alignment, slower but much more accurate
df = DeepFace.find(blank_image, db_path=FACES_FOLDER_FILE_PATH, silent=False, detector_backend='retinaface', align=True, model_name='Facenet512', refresh_database=True)

# No alignment, fast but not as accurate
# df = DeepFace.find(blank_image, db_path=FACES_FOLDER_FILE_PATH, silent=False, model_name='Facenet512', threshold=0.3)