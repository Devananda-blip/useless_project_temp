import io
import time
import numpy as np
from PIL import Image, ImageFilter
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
        pil_img = Image.open(io.BytesIO(image_bytes)).convert('L')
    except Exception as e:
        print("Image Read Error:", e)
        return 0

    # Resize for faster processing while keeping aspect
    max_dim = 800
    w, h = pil_img.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        pil_img = pil_img.resize((int(w * scale), int(h * scale)))

    # Slight blur to reduce noise
    pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=1))
    arr = np.array(pil_img)

    # Simple global threshold (works for most clear-background images)
    thresh_val = arr.mean() + arr.std() * 0.2
    bw = arr > thresh_val

    # Connected-component labeling (stack-based flood fill)
    h, w = bw.shape
    visited = np.zeros((h, w), dtype=bool)
    count = 0
    min_area = 10
    max_area = 5000

    for y in range(h):
        for x in range(w):
            if bw[y, x] and not visited[y, x]:
                # flood fill
                stack = [(y, x)]
                visited[y, x] = True
                area = 0
                while stack:
                    cy, cx = stack.pop()
                    area += 1
                    # 4-neighbors
                    if cy > 0 and bw[cy - 1, cx] and not visited[cy - 1, cx]:
                        visited[cy - 1, cx] = True
                        stack.append((cy - 1, cx))
                    if cy + 1 < h and bw[cy + 1, cx] and not visited[cy + 1, cx]:
                        visited[cy + 1, cx] = True
                        stack.append((cy + 1, cx))
                    if cx > 0 and bw[cy, cx - 1] and not visited[cy, cx - 1]:
                        visited[cy, cx - 1] = True
                        stack.append((cy, cx - 1))
                    if cx + 1 < w and bw[cy, cx + 1] and not visited[cy, cx + 1]:
                        visited[cy, cx + 1] = True
                        stack.append((cy, cx + 1))

                if min_area < area < max_area:
                    count += 1

    return count

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
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)