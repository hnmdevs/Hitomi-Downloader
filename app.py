#!/usr/bin/env python3
"""
Imoogle Downloader - Modern Web-based Media Downloader
A beautiful, fast, and extensible downloader for images and media from 70+ websites.
"""

import os
import sys
import json
import threading
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import requests
from werkzeug.utils import secure_filename

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'imoogle_downloader_secret_key_2024'

# For Vercel, we'll use /tmp for temporary storage
app.config['DOWNLOAD_FOLDER'] = '/tmp/downloads' if os.environ.get('VERCEL') else os.path.join(os.getcwd(), 'downloads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure download directory exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Supported extractors mapping (simplified for Vercel)
EXTRACTORS = {
    'imgur.com': 'imgur',
    'instagram.com': 'instagram', 
    'pinterest.com': 'pinterest',
    'reddit.com': 'reddit',
    'twitter.com': 'twitter',
    'youtube.com': 'youtube',
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
    
    def complete_download(self, task_id, success=True):
        """Mark download as completed"""
        if task_id in self.active_downloads:
            self.active_downloads[task_id]['status'] = 'completed' if success else 'failed'
            self.active_downloads[task_id]['progress'] = 100 if success else 0

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
        return jsonify({'error': f'Site {domain} is not supported yet. Supported sites: {", ".join(EXTRACTORS.keys())}'}), 400
    
    # For Vercel demo, we'll simulate the download process
    task_id = download_manager.add_download(url, options)
    
    # Simulate download completion
    download_manager.update_progress(task_id, 100, 'completed')
    download_manager.complete_download(task_id, True)
    
    return jsonify({
        'task_id': task_id,
        'status': 'completed',
        'message': 'Download completed successfully (Demo mode)',
        'demo': True
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

@app.route('/api/supported-sites')
def api_supported_sites():
    """Get list of supported sites"""
    sites = []
    for domain, extractor in EXTRACTORS.items():
        sites.append({
            'domain': domain,
            'name': domain.split('.')[0].title(),
            'extractor': extractor
        })
    
    return jsonify({
        'sites': sites,
        'total': len(sites)
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
        'timestamp': datetime.now().isoformat(),
        'platform': 'vercel' if os.environ.get('VERCEL') else 'local'
    })

@app.route('/demo')
def demo():
    """Demo page showing the application features"""
    return render_template('demo.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Starting Imoogle Downloader...")
    print("📱 Open http://localhost:5000 in your browser")
    print("🔗 API available at http://localhost:5000/api/")
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)