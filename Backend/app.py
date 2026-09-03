import time
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Website-um backend-um connect aavan

def count_rice_grains(image_bytes):
    # 1. Image read cheyyunnu
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return 0

    # 2. Black & White (Grayscale) aakkunnu
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Rice grains highlight cheyyunnu (Thresholding)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 4. Grains separate aakki count cheyyunnu
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Cheriya noise dots ozhivakkan
    valid_contours = [c for c in contours if cv2.contourArea(c) > 10]
    return len(valid_contours)


@app.route('/api/count', methods=['POST'])
def count_rice():
    start_time = time.time()

    # Website-il ninnu photo vannittundo enn check cheyyunnu
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_bytes = file.read()

    # Rice count cheyyunnu
    grain_count = count_rice_grains(image_bytes)

    # Processing time calculation
    time_wasted = max(1, round(time.time() - start_time, 1))

    # Funny response website-lekku ayakkunnu
    return jsonify({
        "success": True,
        "grain_count": grain_count,
        "time_wasted": time_wasted,
        "message": f"Congratulations. You wasted {time_wasted} seconds counting rice."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)