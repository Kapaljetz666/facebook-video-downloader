from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import re
import threading

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

current_download_progress = {}

def progress_hook(d):
    if d['status'] == 'downloading':
        current_download_progress['progress'] = d.get('_percent_str', 'N/A')
    elif d['status'] == 'finished':
        current_download_progress['progress'] = '100%'
    else:
        current_download_progress['progress'] = 'N/A'

def delete_file_after_delay(file_path):
    try:
        os.remove(file_path)
        print(f"Successfully deleted file after delay: {file_path}")
    except OSError as e:
        print(f"OS Error deleting file {file_path} after delay: {e.strerror} (Error Code: {e.errno})")
    except Exception as e:
        print(f"General Error deleting file {file_path} after delay: {e}")

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    # Basic URL validation for Facebook
    if not re.match(r'^(https?://)?(www\.)?(facebook\.com|fb\.watch)/.*$', video_url):
        return jsonify({'error': 'Invalid Facebook video URL'}), 400

    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'progress_hooks': [progress_hook], # For debugging
            'verbose': True,
            'overwrites': True,
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            
            if os.path.exists(file_path):
                thumbnail_url = info_dict.get('thumbnail')
                return jsonify({'message': 'Request successful', 'file_path': os.path.basename(file_path), 'thumbnail_url': thumbnail_url}), 200
            else:
                return jsonify({'error': 'File not found after download'}), 500

    except yt_dlp.DownloadError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

from flask import Flask, request, jsonify, send_file

# ... (rest of your imports and code)

@app.route('/downloaded_files/<filename>', methods=['GET'])
def serve_downloaded_file(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        print(f"Attempting to serve file: {file_path}")
        # Schedule file deletion after 60 seconds
        timer = threading.Timer(60, delete_file_after_delay, args=[file_path])
        timer.start()
        print(f"Scheduled deletion of {file_path} in 60 seconds.")
        return send_file(file_path, as_attachment=True)
    else:
        print(f"File not found for serving: {file_path}")
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(current_download_progress)
