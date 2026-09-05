from flask import Flask, request, jsonify
from flask_cors import CORS
import exiftool
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "Server active!"})

@app.route('/extract-metadata', methods=['POST'])
def extract_metadata():
    # Frontend 'file' ya 'image' dono bhejega toh handle kar lega
    file = request.files.get('file') or request.files.get('image')
    
    if not file or file.filename == '':
        return jsonify({"error": "No file uploaded"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(filepath)[0]
        
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify(metadata), 200

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
