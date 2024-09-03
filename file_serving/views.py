from django.shortcuts import render
from django.http import FileResponse, StreamingHttpResponse, HttpResponse
from django.conf import settings
import os
from wsgiref.util import FileWrapper
import logging

logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse('Hello, world!')

def serve_file(request, filename):
    logger.debug(f"Serving file: {filename}")
    filepath = os.path.join(settings.STATICFILES_DIRS[0], 'files', filename)
    
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return HttpResponse(status=404)

    file_size = os.path.getsize(filepath)

    if request.method == 'HEAD':
        response = HttpResponse()
        response['Content-Length'] = str(file_size)
        response['Content-Type'] = 'application/octet-stream'
        return response

    response = FileResponse(open(filepath, 'rb'), as_attachment=True)
    response['Content-Length'] = str(file_size)
    response['Content-Type'] = 'application/octet-stream'
    response["Content-Disposition"] = f"attachment; filename={filename}"

    return response

def serve_file_stream(request, filename):
    logger.debug(f"Streaming file: {filename}")
    filepath = os.path.join(settings.STATICFILES_DIRS[0], 'files', filename)

    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return HttpResponse(status=404)

    file_size = os.path.getsize(filepath)

    if request.method == 'HEAD':
        response = HttpResponse()
        response['Content-Length'] = str(file_size)
        response['Content-Type'] = 'application/octet-stream'
        return response

    chunk_size = 8192

    response = StreamingHttpResponse(FileWrapper(open(filepath, 'rb'), chunk_size), content_type='application/octet-stream')
    response['Content-Length'] = str(file_size)
    response["Content-Disposition"] = f"attachment; filename={filename}"

    return response
