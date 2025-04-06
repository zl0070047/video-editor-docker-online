from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from src.video_processor import VideoProcessor
import tempfile
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['UPLOAD_FOLDER'] = Path(tempfile.gettempdir()) / 'video-editor-uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(str(filepath))
        
        # 初始化视频处理器
        processor = VideoProcessor()
        processor.load_video(str(filepath))
        
        return jsonify({
            'filename': filename,
            'duration': processor.get_duration(),
            'fps': processor.get_fps()
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/process', methods=['POST'])
def process_video():
    data = request.json
    filename = data.get('filename')
    start_time = float(data.get('start_time', 0))
    end_time = float(data.get('end_time'))
    output_format = data.get('format', 'mp4')
    
    input_path = app.config['UPLOAD_FOLDER'] / secure_filename(filename)
    output_filename = f"output_{Path(filename).stem}.{output_format}"
    output_path = app.config['UPLOAD_FOLDER'] / output_filename
    
    processor = VideoProcessor()
    processor.load_video(str(input_path))
    processor.export_video(str(output_path), start_time, end_time)
    
    return send_file(
        str(output_path),
        as_attachment=True,
        download_name=output_filename
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 