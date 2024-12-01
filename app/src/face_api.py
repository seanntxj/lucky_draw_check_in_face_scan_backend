import base64
import os
from pathlib import Path
import re
from dotenv import load_dotenv
from fastapi import FastAPI, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import numpy as np
import cv2
import json

# Load environment variables from .env file
load_dotenv()

# Get secret key from .env
# SECRET_KEY = os.getenv('SECRET_KEY')
FACES_FOLDER_FILE_PATH = './app/model/'

app = FastAPI()

# origins = ["http://localhost:5173", "https://seanntxj.github.io"]
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def format_base64_for_opencv(input_string):
    match = re.search(r"base64", input_string)
    if match:
        return str(input_string[match.start():]).replace("base64,", "")
    else:
        return input_string

def resize_with_aspect_ratio(image, target_width, target_height):
    """Resize image to fit within target dimensions while maintaining aspect ratio and adding black padding."""
    h, w = image.shape[:2]
    scale = min(target_width / w, target_height / h)
    new_w, new_h = int(w * scale), int(h * scale)

    # Resize the image
    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Create a black canvas of the target size
    result = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    # Calculate padding to center the image
    top = (target_height - new_h) // 2
    left = (target_width - new_w) // 2

    # Place the resized image onto the canvas
    result[top:top + new_h, left:left + new_w] = resized_image
    return result

def check_face(frame):
    potential_ids_of_person = []
    try:
        # Using RetinaFace alignment, slower but much more accurate
        df = DeepFace.find(frame, db_path=FACES_FOLDER_FILE_PATH, silent=True, detector_backend='retinaface', align=True, model_name='Facenet512', refresh_database=False)
        
        # No alignment, fast but not as accurate
        # df = DeepFace.find(frame, db_path=FACES_FOLDER_FILE_PATH, silent=True, model_name='Facenet512', threshold=0.3)
        try: 
            print(df[0].head(n=10))
            for i in range(len(df[0].head(n=10))):
                try:
                    id_of_person = Path(str(df[0].iloc[i].identity)).parts[-2] 
                except IndexError:
                    # If path doesn't split properly 
                    id_of_person = str(df[0].iloc[i].identity).split('\\')[-2]
                if id_of_person not in potential_ids_of_person: potential_ids_of_person.append(id_of_person)
            return potential_ids_of_person
        except Exception as e: 
            print(f'Error: {e}')
            return []
    except ValueError as e:
        print(f'No face detected: {e}')
        return [] # No face detected

@app.get("/")
def base():
    return "On"

@app.get("/status")
def status():
    return "On"

@app.post("/check-face")
async def check(request: Request):
    try:
        body = await request.json()
        image_in_base64 = body.get("image")
        image_in_base64 = format_base64_for_opencv(image_in_base64)
        if not image_in_base64:
            return JSONResponse({"error": "Missing 'image' field"}, status_code=400)
        
        # Decode base64 string to bytes
        im_bytes = base64.b64decode(image_in_base64)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        # Sanity check images are being decoded properly
        # cv2.imshow('Decoded Image', img)
        # cv2.waitKey(2)  # Wait for a key press (0 means indefinitely)
        # cv2.destroyAllWindows()

        # Get the potential IDs of the person
        potential_ids_of_person = check_face(img)
        return {"potential_ids": potential_ids_of_person}
    
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
@app.post("/check-face-new")
async def check_new(file: UploadFile = File(...), resize: bool = Query(default=True)):
    try:
        # Read the uploaded file's contents
        file_bytes = await file.read()
        
        # Convert file bytes to numpy array and decode image
        im_arr = np.frombuffer(file_bytes, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image format")
        
        # Optionally resize the image
        if resize:
            img = resize_with_aspect_ratio(img, 640, 480)

        # Call your face-checking logic
        potential_ids_of_person = check_face(img)
        return {"potential_ids": potential_ids_of_person}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
	
if __name__ == "__main__":
    import uvicorn
    print('Deepface home directory:', os.environ['DEEPFACE_HOME'])
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=9001
    )
