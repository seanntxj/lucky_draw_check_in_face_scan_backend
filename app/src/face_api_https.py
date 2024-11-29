from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
import cv2
import numpy as np
import json
from dotenv import load_dotenv
from face_api import check_face, format_base64_for_opencv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, Network!"})

@app.route('/check-face', methods=['POST'])
def check_face_endpoint():
    try:
        body = request.get_json()
        if not body:
            return jsonify({"error": "Invalid JSON"}), 400
        
        image_in_base64 = body.get("image")
        if not image_in_base64:
            return jsonify({"error": "Missing 'image' field"}), 400

        image_in_base64 = format_base64_for_opencv(image_in_base64)
        if not image_in_base64:
            return jsonify({"error": "Invalid 'image' format"}), 400
        
        # Decode base64 string to bytes
        im_bytes = base64.b64decode(image_in_base64)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        # Sanity check (optional, commented out)
        # cv2.imshow('Decoded Image', img)
        # cv2.waitKey(2)  # Wait for a key press (0 means indefinitely)
        # cv2.destroyAllWindows()

        # Get the potential IDs of the person
        potential_ids_of_person = check_face(img)
        return jsonify({"potential_ids": potential_ids_of_person})
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, ssl_context=('./app/https_certs/cert.crt', './app/https_certs/cert.key'))
