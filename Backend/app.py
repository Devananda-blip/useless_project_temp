import io
import time
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

def count_rice_grains(image_bytes):
    try:
        # Pillow handles JPG, PNG, WEBP, AVIF, etc.
        pil_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = np.array(pil_img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print("Image Read Error:", e)
        return 0

    if img is None:
        return 0

    # Grayscale & Blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Thresholding for isolating grains
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Contour Detection
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out noise/background spots by area
    valid_contours = [c for c in contours if 10 < cv2.contourArea(c) < 5000]

    return len(valid_contours)

@app.route('/api/count', methods=['POST'])
def count():
    start_time = time.time()

    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No image selected'}), 400

    image_bytes = file.read()
    grain_count = count_rice_grains(image_bytes)

    elapsed_time = round(time.time() - start_time, 2)
    message = f"Congratulations. You wasted {elapsed_time} seconds counting rice."

    return jsonify({
        'success': True,
        'grain_count': grain_count,
        'time_wasted': elapsed_time,
        'message': message
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)