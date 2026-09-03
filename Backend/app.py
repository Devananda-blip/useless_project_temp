import io
import time
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_malayalam_dialogue(count):
    """
    Rice count anusarichu funny dialogue and tier set cheyyunna function.
    """
    if count == 0:
        return {
            "dialogue": "Idhenthuvadey... Ari evide? odriiiiiii! 🧐",
            "tier": "zero",
            "movie_ref": "Dasan & Vijayan"
        }
    elif count <= 100:
        return {
            "dialogue": "Ithra cheriya ennathinaano thaan samayam kalanjath? 100 ari polum illa! 😂",
            "tier": "low",
            "movie_ref": "Casual Comedy"
        }
    elif count <= 500:
        return {
            "dialogue": "Aaha, oru pidi chorinnulla ariyundu! Sadharanakkaaranu ith dhaaralam! 🍚",
            "tier": "medium",
            "movie_ref": "Ordinary Rice"
        }
    elif count <= 1000:
        return {
            "dialogue": "Ninakku choru venoda choru?! Enthino vendi thilakkunna sambaar! 🥘🔥",
            "tier": "innocent",
            "movie_ref": "Innocent Iconic"
        }
    elif count <= 1500:
        return {
            "dialogue": "Ente ponno! Enthadey ith, ration kadayanao? Ithra ariyo! 😲💥",
            "tier": "salimkumar",
            "movie_ref": "Salim Kumar Mode"
        }
    else:
        return {
            "dialogue": "Alavatta ari saagaram! Oru naattukaare muzhuvan oottanulla ari undallo aliya! 🥳🎉",
            "tier": "ultra_legend",
            "movie_ref": "Jagathy & Ashokan"
        }

def count_rice_grains(image_bytes):
    try:
        pil_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = np.array(pil_img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print("Image Read Error:", e)
        return 0

    if img is None:
        return 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

    # Dialogue logic call cheyyunnu
    dialogue_info = get_malayalam_dialogue(grain_count)

    return jsonify({
        'success': True,
        'grain_count': grain_count,
        'time_wasted': elapsed_time,
        'dialogue': dialogue_info['dialogue'],
        'tier': dialogue_info['tier'],
        'movie_ref': dialogue_info['movie_ref'],
        'message': f"You wasted {elapsed_time} seconds counting {grain_count} rice grains!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)