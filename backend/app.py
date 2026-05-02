import os
import uuid
import zipfile
import traceback
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from services.batch_processor import BatchProcessor
from services.watermark import WatermarkService
from utils.file_handler import FileHandler

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, '..', 'outputs')
TEMP_FOLDER = os.path.join(BASE_DIR, '..', 'temp')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

ALLOWED_EXTENSIONS = {'py', 'ipynb', 'c', 'html', 'htm', 'txt', 'cpp', 'java', 'js', 'css'}

batch_processor = BatchProcessor(OUTPUT_FOLDER, TEMP_FOLDER)
watermark_service = WatermarkService()
file_handler = FileHandler(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})


@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No files selected'}), 400

    uploaded = []
    errors = []

    for file in files:
        if file.filename == '':
            continue
        if not allowed_file(file.filename):
            errors.append({'filename': file.filename, 'error': 'File type not supported'})
            continue
        try:
            original_name = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())[:8]
            saved_name = f"{unique_id}_{original_name}"
            save_path = os.path.join(UPLOAD_FOLDER, saved_name)
            file.save(save_path)
            uploaded.append({
                'id': unique_id,
                'original_name': original_name,
                'saved_name': saved_name,
                'size': os.path.getsize(save_path),
                'extension': original_name.rsplit('.', 1)[1].lower()
            })
        except Exception as e:
            errors.append({'filename': file.filename, 'error': str(e)})

    return jsonify({
        'uploaded': uploaded,
        'errors': errors,
        'message': f'{len(uploaded)} file(s) uploaded successfully'
    })


@app.route('/api/convert', methods=['POST'])
def convert_files():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    file_list = data.get('files', [])
    watermark_config = data.get('watermark', {})

    if not file_list:
        return jsonify({'error': 'No files specified for conversion'}), 400

    results = []
    errors = []

    for file_info in file_list:
        saved_name = file_info.get('saved_name')
        original_name = file_info.get('original_name')
        file_path = os.path.join(UPLOAD_FOLDER, saved_name)

        if not os.path.exists(file_path):
            errors.append({'filename': original_name, 'error': 'File not found on server'})
            continue

        try:
            output_name = original_name.rsplit('.', 1)[0] + '.pdf'
            unique_id = file_info.get('id', str(uuid.uuid4())[:8])
            output_name = f"{unique_id}_{output_name}"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            batch_processor.convert_file(file_path, output_path)

            if watermark_config.get('enabled') and os.path.exists(output_path):
                watermark_service.apply_watermark(
                    pdf_path=output_path,
                    text=watermark_config.get('text', 'CONFIDENTIAL'),
                    position=watermark_config.get('position', 'center'),
                    opacity=float(watermark_config.get('opacity', 0.3)),
                    font_size=int(watermark_config.get('font_size', 48))
                )

            results.append({
                'original_name': original_name,
                'output_name': output_name,
                'status': 'success'
            })

        except Exception as e:
            traceback.print_exc()
            errors.append({'filename': original_name, 'error': str(e)})

    return jsonify({
        'results': results,
        'errors': errors,
        'message': f'{len(results)} file(s) converted successfully'
    })


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, as_attachment=True, download_name=filename)


@app.route('/api/download-zip', methods=['POST'])
def download_zip():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    output_files = data.get('files', [])
    if not output_files:
        return jsonify({'error': 'No files specified'}), 400

    zip_name = f"converted_{str(uuid.uuid4())[:8]}.zip"
    zip_path = os.path.join(TEMP_FOLDER, zip_name)

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for output_name in output_files:
                file_path = os.path.join(OUTPUT_FOLDER, output_name)
                if os.path.exists(file_path):
                    display_name = '_'.join(output_name.split('_')[1:]) if '_' in output_name else output_name
                    zf.write(file_path, display_name)

        return send_file(zip_path, as_attachment=True, download_name='converted_files.zip')
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/cleanup', methods=['POST'])
def cleanup_files():
    data = request.get_json() or {}
    file_ids = data.get('ids', [])

    cleaned = 0
    for file_id in file_ids:
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            for fname in os.listdir(folder):
                if fname.startswith(file_id + '_'):
                    try:
                        os.remove(os.path.join(folder, fname))
                        cleaned += 1
                    except Exception:
                        pass

    return jsonify({'message': f'Cleaned up {cleaned} file(s)'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
