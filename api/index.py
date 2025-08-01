#!/usr/bin/env python3
"""
Vercel entry point for Imoogle Downloader
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our app
sys.path.append(str(Path(__file__).parent.parent))

# Import the Flask app from the main app.py
from app import app

# Vercel expects the app to be available as 'app' or a callable
# The app is already configured in app.py, so we just need to export it
if __name__ == "__main__":
    app.run()