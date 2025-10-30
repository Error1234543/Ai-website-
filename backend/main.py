import os
import json
import base64
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# CONFIG
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PORT = int(os.getenv("PORT", 8000))

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is required. Put it in environment or .env file.")

app = Flask(__name__, static_folder="frontend", static_url_path="/")
CORS(app, origins="*")

# endpoints to try (fallbacks)
GEMINI_ENDPOINTS = [
    "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}",
    "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={key}",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={key}",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={key}",
]

def call_gemini(payload):
    last_err = None
    for tmpl in GEMINI_ENDPOINTS:
        url = tmpl.format(key=GEMINI_API_KEY)
        try:
            res = requests.post(url, json=payload, timeout=60)
            if res.status_code == 200:
                return res.json()
            else:
                last_err = Exception(f"{res.status_code}: {res.text}")
        except Exception as e:
            last_err = e
    raise last_err

def extract_text(data):
    try:
        return data.get('candidates', [])[0].get('content', {}).get('parts', [])[0].get('text')
    except Exception:
        return json.dumps(data)[:3000]

@app.route('/api/chat', methods=['POST'])
def api_chat():
    body = request.json or {}
    prompt = body.get('prompt', '').strip()
    if not prompt:
        return jsonify({'ok': False, 'error': 'prompt required'}), 400
    payload = { 'contents': [ { 'parts': [ { 'text': prompt } ] } ] }
    try:
        data = call_gemini(payload)
        return jsonify({'ok': True, 'text': extract_text(data)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/image', methods=['POST'])
def api_image():
    prompt = request.form.get('prompt', 'Solve or explain the question in the image step-by-step:')
    img = request.files.get('image')
    if img is None:
        return jsonify({'ok': False, 'error': 'image required'}), 400
    b = img.read()
    b64 = base64.b64encode(b).decode('utf-8')
    contents = [{ 'parts': [ { 'inline_data': { 'mime_type': img.mimetype or 'image/jpeg', 'data': b64 } }, { 'text': prompt } ] }]
    payload = {'contents': contents}
    try:
        data = call_gemini(payload)
        return jsonify({'ok': True, 'text': extract_text(data)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# serve frontend for local testing (optional)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/health')
def health():
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
