from flask import Flask, render_template, request, jsonify, send_file # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import os
import logging
from src.video_processor import VideoProcessor
import tempfile
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)

# 基本配置
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    UPLOAD_FOLDER=Path(tempfile.gettempdir()) / 'video-editor-uploads'
)

# 确保上传目录存在
app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)
logging.info(f"Upload directory: {app.config['UPLOAD_FOLDER']}")

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """健康检查端点"""
    upload_dir = app.config['UPLOAD_FOLDER']
    health_status = {
        'status': 'healthy',
        'upload_dir': str(upload_dir),
        'upload_dir_exists': upload_dir.exists(),
        'upload_dir_writable': os.access(upload_dir, os.W_OK),
        'environment': os.environ.get('FLASK_ENV', 'development')
    }
    logging.info(f"Health check: {health_status}")
    return jsonify(health_status)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = app.config['UPLOAD_FOLDER'] / filename
            file.save(str(filepath))
            logging.info(f"File saved: {filepath}")
            
            # 初始化视频处理器
            processor = VideoProcessor()
            if not processor.open_video(str(filepath)):
                return jsonify({'error': 'Failed to open video'}), 400
            
            return jsonify({
                'filename': filename,
                'duration': processor.get_duration(),
                'fps': processor.get_fps()
            })
        except Exception as e:
            logging.error(f"Upload error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/process', methods=['POST'])
def process_video():
    try:
        data = request.json
        filename = data.get('filename')
        start_time = float(data.get('start_time', 0))
        end_time = float(data.get('end_time'))
        output_format = data.get('output_format', 'mp4')
        
        input_path = app.config['UPLOAD_FOLDER'] / secure_filename(filename)
        output_filename = f"output_{Path(filename).stem}.{output_format}"
        output_path = app.config['UPLOAD_FOLDER'] / output_filename
        
        logging.info(f"Processing video: {input_path} -> {output_path}")
        
        processor = VideoProcessor()
        if not processor.open_video(str(input_path)):
            return jsonify({'error': 'Failed to open video'}), 400
            
        if not processor.export_video(str(output_path), start_time, end_time):
            return jsonify({'error': 'Failed to process video'}), 500
        
        return send_file(
            str(output_path),
            as_attachment=True,
            download_name=output_filename
        )
    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 