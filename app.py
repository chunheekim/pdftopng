from flask import Flask, render_template, request, jsonify, send_from_directory
from pdf2image import convert_from_path
from PIL import Image
import os
import uuid

app = Flask(__name__)

# 변환된 이미지 저장 폴더
OUTPUT_FOLDER = 'static/converted'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdf_file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 파일 저장
    unique_id = str(uuid.uuid4())
    pdf_path = f'{OUTPUT_FOLDER}/{unique_id}.pdf'
    file.save(pdf_path)

    # PDF → PNG 변환
    try:
        images = convert_from_path(pdf_path)
        png_urls = []

        for i, image in enumerate(images):
            png_filename = f'{unique_id}_page_{i + 1}.png'
            png_path = os.path.join(OUTPUT_FOLDER, png_filename)
            image.save(png_path, 'PNG')

            png_urls.append(f'/{OUTPUT_FOLDER}/{png_filename}')

        os.remove(pdf_path)  # PDF 원본 삭제해도 되고 안 해도 됨

        return jsonify({'png_urls': png_urls})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 정적 파일 다운로드용 라우트 (필요한 경우)
@app.route('/static/converted/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
