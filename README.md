<p align="center">
  <img src="imgs/imoogle_logo.png" width="50%"/>
  <br>
  <h1>🖼️ Imoogle Downloader</h1>
  <p><em>A powerful, modern image and media downloader supporting 70+ websites</em></p>
</p>

[![GitHub release](https://img.shields.io/github/release/KurtBestor/Imoogle-Downloader.svg?logo=github)](https://github.com/KurtBestor/Imoogle-Downloader/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/KurtBestor/Imoogle-Downloader/latest/total.svg?logo=github)](https://github.com/KurtBestor/Imoogle-Downloader/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/KurtBestor/Imoogle-Downloader/total.svg?logo=github)](https://github.com/KurtBestor/Imoogle-Downloader/releases)

## 🚀 Quick Start
- [Web App](http://localhost:5000) - Run locally with `python app.py`
- [Download Desktop Version](https://github.com/KurtBestor/Imoogle-Downloader/releases/latest)
- [Issues & Support](https://github.com/KurtBestor/Imoogle-Downloader/issues)
- [Chrome Extension](https://github.com/KurtBestor/Imoogle-Downloader/wiki/Chrome-Extension)

## 🎯 Demo
<img src="imgs/imoogle_demo.gif">

## ✨ Features
- 🌐 **Modern Web Interface** - Clean, responsive design
- 🖼️ **Image-First Focus** - Optimized for image galleries and collections
- 🚀 **Lightning Fast** - Multi-threaded downloads (up to 24 threads)
- 📱 **Mobile Friendly** - Works on all devices
- 🎨 **Beautiful UI** - Dark/light mode support
- 📋 **Smart Detection** - Automatic URL parsing and content detection
- 🔄 **Batch Downloads** - Queue multiple URLs
- 📊 **Progress Tracking** - Real-time download progress
- 🗂️ **Auto Organization** - Smart file naming and folder structure
- 🌙 **Dark Mode** - Easy on the eyes
- 🔧 **Extensible** - Plugin system for custom extractors

## 🌍 Supported Sites
| Site | Focus | URL |
| :--: | :--: | -- |
| **Instagram** | 📸 Photos/Stories | <https://instagram.com> |
| **Pinterest** | 🎨 Images/Boards | <https://pinterest.com> |
| **Imgur** | 🖼️ Image Hosting | <https://imgur.com> |
| **DeviantArt** | 🎨 Digital Art | <https://deviantart.com> |
| **ArtStation** | 🎨 Professional Art | <https://artstation.com> |
| **Flickr** | 📷 Photography | <https://flickr.com> |
| **Pixiv** | 🎨 Anime/Manga Art | <https://pixiv.net> |
| **Tumblr** | 📱 Multimedia Blog | <https://tumblr.com> |
| **Twitter** | 🐦 Social Media | <https://twitter.com> |
| **Facebook** | 📘 Social Network | <https://facebook.com> |
| **YouTube** | 🎥 Video Platform | <https://youtube.com> |
| **TikTok** | 🎵 Short Videos | <https://tiktok.com> |
| **Twitch** | 🎮 Live Streaming | <https://twitch.tv> |
| **Reddit** | 💬 Discussion Forum | <https://reddit.com> |
| **and 50+ more...** | 🌐 | [Full list of supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) |

## 🛠️ Installation & Deployment

### Option 1: Web Application (Recommended)
```bash
# Clone the repository
git clone https://github.com/KurtBestor/Imoogle-Downloader.git
cd Imoogle-Downloader

# Install dependencies
pip install -r requirements.txt

# Run the web app
python app.py
```
Then open http://localhost:5000 in your browser.

### Option 2: Docker Deployment
```bash
# Build and run with Docker
docker build -t imoogle-downloader .
docker run -p 5000:5000 -v $(pwd)/downloads:/app/downloads imoogle-downloader
```

### Option 3: Cloud Deployment
- **Heroku**: One-click deploy button available
- **Railway**: Deploy with `railway up`
- **Vercel**: Serverless deployment ready
- **DigitalOcean**: App Platform compatible

## 🎯 Usage Examples

### Web Interface
1. Open http://localhost:5000
2. Paste any supported URL
3. Choose download options
4. Click "Download" and watch the magic happen!

### API Usage
```bash
# Download via API
curl -X POST http://localhost:5000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://instagram.com/p/example"}'
```

## 🤝 Contributing
We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- Built on the foundation of Hitomi Downloader
- Powered by yt-dlp for video extraction
- UI inspired by modern design principles
