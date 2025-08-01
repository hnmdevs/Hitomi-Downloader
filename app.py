#!/usr/bin/env python3
"""
Imoogle Downloader - Modern Web-based Media Downloader
A beautiful, fast, and extensible downloader for images and media from 70+ websites.
"""

import os
import sys
import json
import asyncio
import threading
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_socketio import SocketIO, emit
import requests
from werkzeug.utils import secure_filename

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our extractors
from src.extractor import imgur_downloader, instagram_downloader, pinterest_downloader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'imoogle_downloader_secret_key_2024'
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.getcwd(), 'downloads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Ensure download directory exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Supported extractors mapping
EXTRACTORS = {
    'imgur.com': imgur_downloader,
    'instagram.com': instagram_downloader,
    'pinterest.com': pinterest_downloader,
    # Add more as needed
}

class DownloadManager:
    """Manages download tasks and progress tracking"""
    
    def __init__(self):
        self.active_downloads = {}
        self.download_history = []
    
    def add_download(self, url, options=None):
        """Add a new download task"""
        task_id = f"task_{len(self.download_history) + 1}_{int(datetime.now().timestamp())}"
        
        task = {
            'id': task_id,
            'url': url,
            'status': 'pending',
            'progress': 0,
            'total_files': 0,
            'downloaded_files': 0,
            'created_at': datetime.now().isoformat(),
            'options': options or {}
        }
        
        self.active_downloads[task_id] = task
        self.download_history.append(task)
        
        return task_id
    
    def update_progress(self, task_id, progress, status=None):
        """Update download progress"""
        if task_id in self.active_downloads:
            self.active_downloads[task_id]['progress'] = progress
            if status:
                self.active_downloads[task_id]['status'] = status
            
            # Emit progress update via SocketIO
            socketio.emit('download_progress', {
                'task_id': task_id,
                'progress': progress,
                'status': status or self.active_downloads[task_id]['status']
            })
    
    def complete_download(self, task_id, success=True):
        """Mark download as completed"""
        if task_id in self.active_downloads:
            self.active_downloads[task_id]['status'] = 'completed' if success else 'failed'
            self.active_downloads[task_id]['progress'] = 100 if success else 0
            
            socketio.emit('download_complete', {
                'task_id': task_id,
                'success': success
            })

# Global download manager instance
download_manager = DownloadManager()

@app.route('/')
def index():
    """Main page with the downloader interface"""
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def api_download():
    """API endpoint to start a download"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url'].strip()
    options = data.get('options', {})
    
    # Validate URL
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return jsonify({'error': 'Invalid URL format'}), 400
    except Exception:
        return jsonify({'error': 'Invalid URL'}), 400
    
    # Check if we support this site
    domain = parsed.netloc.lower().replace('www.', '')
    if domain not in EXTRACTORS:
        return jsonify({'error': f'Site {domain} is not supported yet'}), 400
    
    # Start download task
    task_id = download_manager.add_download(url, options)
    
    # Start download in background thread
    thread = threading.Thread(target=process_download, args=(task_id, url, options))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'task_id': task_id,
        'status': 'started',
        'message': 'Download started successfully'
    })

@app.route('/api/status/<task_id>')
def api_status(task_id):
    """Get download status"""
    if task_id in download_manager.active_downloads:
        return jsonify(download_manager.active_downloads[task_id])
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/api/history')
def api_history():
    """Get download history"""
    return jsonify({
        'downloads': download_manager.download_history[-50:],  # Last 50 downloads
        'total': len(download_manager.download_history)
    })

@app.route('/downloads/<path:filename>')
def download_file(filename):
    """Serve downloaded files"""
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

def process_download(task_id, url, options):
    """Process download in background thread"""
    try:
        download_manager.update_progress(task_id, 10, 'initializing')
        
        # Parse domain and get appropriate extractor
        domain = urlparse(url).netloc.lower().replace('www.', '')
        extractor_module = EXTRACTORS.get(domain)
        
        if not extractor_module:
            download_manager.complete_download(task_id, False)
            return
        
        download_manager.update_progress(task_id, 30, 'extracting')
        
        # Create download folder for this task
        task_folder = os.path.join(app.config['DOWNLOAD_FOLDER'], task_id)
        os.makedirs(task_folder, exist_ok=True)
        
        download_manager.update_progress(task_id, 50, 'downloading')
        
        # Simulate download process (replace with actual extractor logic)
        import time
        for i in range(50, 100, 10):
            time.sleep(0.5)  # Simulate work
            download_manager.update_progress(task_id, i, 'downloading')
        
        download_manager.complete_download(task_id, True)
        
    except Exception as e:
        print(f"Download error for task {task_id}: {str(e)}")
        download_manager.complete_download(task_id, False)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to Imoogle Downloader'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Starting Imoogle Downloader...")
    print("📱 Open http://localhost:5000 in your browser")
    print("🔗 API available at http://localhost:5000/api/")
    
    # Run the app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)