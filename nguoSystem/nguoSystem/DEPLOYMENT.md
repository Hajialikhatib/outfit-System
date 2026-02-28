# Nguo System - Deployment Guide

This guide covers deploying the Nguo System to a production server.

## Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Nginx
- Git

## Deployment Steps

### 1. Server Setup

```
bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, Node.js, and dependencies
sudo apt install -y python3 python3-venv python3-pip nodejs npm mysql-server nginx

# Install MySQL client library (required for mysqlclient)
sudo apt install -y default-libmysqlclient-dev build-essential pkg-config
```

### 2. Clone and Setup

```
bash
# Clone the repository
cd /var/www
git clone https://github.com/your-repo/nguoSystem.git
cd nguoSystem

# Copy and configure environment variables
cp .env.example .env
# Edit .env with production values
nano .env
```

### 3. Configure .env File

Edit the `.env` file with production values:

```
env
# Django Settings
SECRET_KEY=generate-a-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ENVIRONMENT=production

# Database
DB_NAME=nguo_system
DB_USER=nguo_user
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=3306

# CORS (your production frontend URL)
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### 4. Backend Setup

```
bash
cd backend

# Create virtual environment
python3 -m venv ../.venv
source ../.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

### 5. Frontend Setup

```
bash
cd ../frontend

# Create .env file for production
echo "VITE_API_BASE_URL=https://yourdomain.com/api" > .env

# Install dependencies
npm install

# Build for production
npm run build
```

### 6. Nginx Configuration

```
bash
# Copy nginx configuration
sudo cp /var/www/nguoSystem/nginx.conf /etc/nginx/sites-available/nguoSystem
sudo ln -s /etc/nginx/sites-available/nguoSystem /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 7. Start Services

```
bash
# Start Gunicorn (using the production script)
cd /var/www/nguoSystem/backend
source ../.venv/bin/activate
gunicorn -c gunicorn_config.py nguoSystem.wsgi:application

# Or use systemd service (recommended)
# Create /etc/systemd/system/nguoSystem.service
```

### 8. Systemd Service (Recommended)

Create `/etc/systemd/system/nguoSystem.service`:

```
ini
[Unit]
Description=Nguo System Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/nguoSystem/backend
Environment="PATH=/var/www/nguoSystem/.venv/bin"
Environment="ENVIRONMENT=production"
ExecStart=/var/www/nguoSystem/.venv/bin/gunicorn -c gunicorn_config.py nguoSystem.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

```
bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable nguoSystem
sudo systemctl start nguoSystem
```

## Directory Structure

```
/var/www/nguoSystem/
├── backend/
│   ├── nguoSystem/          # Django project
│   ├── accounts/           # User accounts app
│   ├── styles/            # Styles app
│   ├── orders/            # Orders app
│   ├── feedback/          # Feedback app
│   ├── media/             # User uploads
│   ├── staticfiles/       # Django static files
│   ├── gunicorn_config.py
│   └── requirements.txt
├── frontend/
│   ├── dist/              # Built static files
│   └── src/               # React source
├── nginx.conf
├── .env
└── .venv/                 # Python virtual environment
```

## Troubleshooting

### Check Gunicorn logs
```
bash
sudo journalctl -u nguoSystem -f
```

### Check Nginx logs
```
bash
sudo tail -f /var/log/nginx/error.log
```

### Common Issues

1. **502 Bad Gateway**: Check if Gunicorn is running
2. **Static files not loading**: Run `collectstatic` and check nginx alias paths
3. **Database connection error**: Verify database credentials in `.env`
4. **CORS errors**: Ensure CORS_ALLOWED_ORIGINS includes your frontend domain

## Security Checklist

- [ ] Set DEBUG=False in production
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set up firewall (ufw)
- [ ] Regular backups of database
- [ ] Keep dependencies updated
