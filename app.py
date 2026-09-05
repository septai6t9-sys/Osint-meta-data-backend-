from flask import Flask, request, jsonify
from flask_cors import CORS
import exiftool
import os

app = Flask(__name__)

# CORS enable kar rahe hain taaki kisi bhi frontend website se request aa sake
CORS(app)

# Uploaded files ko temporary save karne ke liye folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "Server is running successfully!"})

@app.route('/extract-metadata', methods=['POST'])
def extract_metadata():
    # Check karna ki request mein image file aayi hai ya nahi
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Image ko temporary save karna
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        # ExifTool se metadata extract karna
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(filepath)[0]
        
        # Metadata nikalne ke baad file ko server se delete kar dena (Memory clean rakhne ke liye)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            "status": "success",
            "metadata": metadata
        }), 200

    except Exception as e:
        # Agar koi error aaye toh bhi temporary file delete kar dena
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
