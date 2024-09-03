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
