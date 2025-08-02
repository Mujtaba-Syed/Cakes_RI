# Cakes RI - Deployment Guide

## Quick Deployment

### 1. Upload to Server
```bash
# From your local project directory
scp -r . root@77.37.47.26:/app/cakes/
```

### 2. Deploy on Server
```bash
ssh root@77.37.47.26
cd /app/cakes
chmod +x deploy.sh
./deploy.sh
```

### 3. Access Your Site
- **URL:** http://cakebyrimi.com:8002
- **Your existing site:** https://qhenterprises.com

## Files Explained

- **`docker-compose.yml`** - Runs your Django app on port 8001 and nginx on port 8002
- **`nginx/cakes.conf`** - Nginx configuration for your cake project
- **`deploy.sh`** - Simple deployment script
- **`nginx/django.conf`** - Old config (not used)

## DNS Setup Required

Make sure your domain `cakebyrimi.com` points to `77.37.47.26`:
- A record: `@` → `77.37.47.26`
- A record: `www` → `77.37.47.26`

That's it! Simple and clean. 🎂 