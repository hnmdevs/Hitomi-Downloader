# 🚀 Imoogle Downloader Deployment Guide

This guide covers multiple deployment options for the Imoogle Downloader application.

## 📋 Prerequisites

- Python 3.8+ (for local deployment)
- Docker & Docker Compose (for containerized deployment)
- Git

## 🏠 Local Development Deployment

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-username/Imoogle-Downloader.git
cd Imoogle-Downloader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

### Environment Variables
```bash
export FLASK_ENV=development  # or production
export FLASK_DEBUG=1          # for development only
export SECRET_KEY=your-secret-key-here
export DOWNLOAD_FOLDER=/path/to/downloads
```

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)
```bash
# Clone and navigate to the project
git clone https://github.com/your-username/Imoogle-Downloader.git
cd Imoogle-Downloader

# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 2: Docker Build & Run
```bash
# Build the image
docker build -t imoogle-downloader .

# Run the container
docker run -d \
  --name imoogle-downloader \
  -p 5000:5000 \
  -v $(pwd)/downloads:/app/downloads \
  imoogle-downloader

# View logs
docker logs -f imoogle-downloader
```

## ☁️ Cloud Deployment Options

### 1. Heroku Deployment

#### Automatic Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/your-username/Imoogle-Downloader)

#### Manual Deploy
```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Open the app
heroku open
```

Create `Procfile`:
```
web: python app.py
```

### 2. Railway Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. DigitalOcean App Platform

1. Fork this repository
2. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
3. Create new app from GitHub repository
4. Configure:
   - **Source**: Your forked repository
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python app.py`
   - **Port**: 5000

### 4. Google Cloud Platform (Cloud Run)

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/imoogle-downloader

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT-ID/imoogle-downloader --platform managed
```

### 5. AWS ECS/Fargate

1. Push image to ECR:
```bash
# Create ECR repository
aws ecr create-repository --repository-name imoogle-downloader

# Build and push
docker build -t imoogle-downloader .
docker tag imoogle-downloader:latest 123456789.dkr.ecr.region.amazonaws.com/imoogle-downloader:latest
docker push 123456789.dkr.ecr.region.amazonaws.com/imoogle-downloader:latest
```

2. Create ECS task definition and service through AWS Console

### 6. Azure Container Instances

```bash
# Create resource group
az group create --name imoogle-rg --location eastus

# Deploy container
az container create \
  --resource-group imoogle-rg \
  --name imoogle-downloader \
  --image your-registry/imoogle-downloader:latest \
  --ports 5000 \
  --environment-variables FLASK_ENV=production
```

## 🌐 Production Configuration

### Nginx Reverse Proxy

Create `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server imoogle-downloader:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket support for real-time updates
        location /socket.io/ {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### SSL/HTTPS Setup

1. **Using Let's Encrypt with Certbot:**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

2. **Using Cloudflare:**
- Point your domain to your server IP
- Enable "Full (Strict)" SSL mode in Cloudflare
- Use Cloudflare's origin certificates

### Environment Variables for Production

```bash
# Security
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-here

# Performance
WORKERS=4
THREADS=2

# Storage
DOWNLOAD_FOLDER=/app/downloads
MAX_CONTENT_LENGTH=104857600  # 100MB

# Database (if using one)
DATABASE_URL=postgresql://user:pass@localhost/imoogle

# External APIs
YOUTUBE_API_KEY=your-api-key
INSTAGRAM_SESSION_ID=your-session-id
```

## 📊 Monitoring & Logging

### Health Checks
The application provides a health check endpoint at `/health`:
```bash
curl http://localhost:5000/health
```

### Logging Configuration
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Prometheus Metrics (Optional)
Add to `requirements.txt`:
```
prometheus-flask-exporter==0.23.0
```

## 🔧 Troubleshooting

### Common Issues

1. **Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

2. **Permission issues with downloads folder:**
```bash
chmod 755 downloads/
chown -R $USER:$USER downloads/
```

3. **Memory issues:**
- Increase Docker memory limit
- Use environment variables to limit concurrent downloads
- Implement download queue system

### Performance Optimization

1. **Use Gunicorn for production:**
```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

2. **Enable gzip compression:**
```python
from flask_compress import Compress
Compress(app)
```

3. **Use Redis for session storage:**
```python
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
```

## 🔐 Security Considerations

1. **Use HTTPS in production**
2. **Set secure session cookies**
3. **Implement rate limiting**
4. **Validate all user inputs**
5. **Use environment variables for secrets**
6. **Regular security updates**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@imoogle-downloader.com
- 💬 Discord: [Join our server](https://discord.gg/imoogle)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/Imoogle-Downloader/issues)
- 📖 Wiki: [Documentation](https://github.com/your-username/Imoogle-Downloader/wiki)