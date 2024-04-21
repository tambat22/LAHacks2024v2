from typing import Union
from fastapi import FastAPI
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def img_to_text(image_path):
    print("Image path: ", image_path)
    return image_path

@app.post("/upload")
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        text = img_to_text(file_path)
        return jsonify({'text': text})

if __name__ == "__main__":
    app.run(debug=True)