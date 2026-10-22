# app.py - KHALED VIP Feedback Server
import os
import base64
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 TELEGRAM BOT AYARLARI
BOT_TOKEN = "8199864222:AAF5nWh9tCl-tcn5I_N6PntBVk5V_tPV3vM"
CHAT_ID = "-1004355323124"

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "KHALED VIP Feedback Server ONLINE",
        "version": "4.0"
    })

@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        if request.content_type and 'application/json' in request.content_type:
            data = request.json or {}
            base64_image = data.get('base64_image', '')
            caption = data.get('caption', '')
        else:
            base64_image = request.form.get('base64_image', '')
            caption = request.form.get('caption', '')

        if not base64_image:
            return jsonify({"status": False, "error": "No image provided"}), 400

        try:
            base64_image = base64_image.replace('%2B', '+').replace('%2F', '/').replace('%3D', '=')
            image_bytes = base64.b64decode(base64_image)
        except Exception as e:
            return jsonify({"status": False, "error": f"Base64 decode failed: {e}"}), 400

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': ('screenshot.jpg', image_bytes, 'image/jpeg')}
        payload = {
            'chat_id': CHAT_ID,
            'caption': caption[:1024],
            'parse_mode': 'HTML'
        }

        response = requests.post(url, data=payload, files=files, timeout=60)

        if response.status_code == 200:
            return jsonify({"status": True, "message": "Sent to Telegram"})
        else:
            return jsonify({"status": False, "error": response.text}), 500

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)