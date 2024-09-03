# download_speed_test

[![Django CI](https://github.com/keyqcloud/download_speed_test/actions/workflows/django.yml/badge.svg)](https://github.com/keyqcloud/download_speed_test/actions/workflows/django.yml)

This Django application serves static files of various sizes and supports multiple stream downloads for the purpose of testing download speeds. The application can be used to measure and compare the performance of single-stream and multi-stream downloads.

## Features

- **Static File Serving**: Serves dummy files of sizes 100MB, 250MB, 500MB, and 1GB.
- **Multi-Stream Download Support**: Allows for testing download speeds with multiple streams.

## Prerequisites

- Python 3.9+
- Django 3.2+
- Gunicorn (for production)
- Nginx (for serving static files and proxying to Gunicorn)
- Puppeteer (for testing download speeds)

## Create dummy static files

```
mkdir -p static/files
dd if=/dev/random of=static/files/100MB.bin bs=1M count=100
dd if=/dev/random of=static/files/250MB.bin bs=1M count=250
dd if=/dev/random of=static/files/500MB.bin bs=1M count=500
dd if=/dev/random of=static/files/1GB.bin bs=1M count=1000
```

## Configure Ngnix

Setup a self-signed certificate
```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx-selfsigned.key -out /etc/nginx/ssl/nginx-selfsigned.crt
sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
```

Create a configuration file at `/etc/nginx/conf.d/download_speed_test_ssl.conf`
```
server {
    listen 443 ssl;
    server_name your_domain_or_IP;  # Replace with your domain name or public IP

    ssl_certificate /etc/nginx/ssl/nginx-selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx-selfsigned.key;
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
    ssl_session_timeout  10m;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off; # Requires nginx >= 1.5.9
    ssl_stapling on; # Requires nginx >= 1.3.7
    ssl_stapling_verify on; # Requires nginx >= 1.3.7
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    ssl_buffer_size 8k;

    location / {
        proxy_pass http://unix:/home/ec2-user/download_speed_test/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ec2-user/download_speed_test/static/;
    }
}
```

Check syntax
```
sudo nginx -t
```

And restart Ngnix
```
sudo systemctl restart nginx
```
