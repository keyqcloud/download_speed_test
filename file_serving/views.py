from django.shortcuts import render
from django.http import FileResponse
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
import os

def serve_file(request, filename):
    filepath = os.path.join(settings.STATICFILES_DIRS[0], 'files', filename)
    return FileResponse(open(filepath, 'rb'), as_attachment=True)

def serve_file_stream(request, filename):
    filepath = os.path.join(settings.STATICFILES_DIRS[0], 'files', filename)

    file_size = os.path.getsize(filepath)
    range_header = request.headers.get('Range', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else file_size - 1

        chunk_size = 8192  # 8KB chunks
        length = last_byte - first_byte + 1

        def stream_file():
            with open(filepath, 'rb') as f:
                f.seek(first_byte)
                while first_byte <= last_byte:
                    bytes_to_read = min(chunk_size, last_byte - first_byte + 1)
                    data = f.read(bytes_to_read)
                    if not data:
                        break
                    yield data
                    first_byte += bytes_to_read

        response = StreamingHttpResponse(stream_file(), status=206, content_type='application/octet-stream')
        response['Content-Length'] = str(length)
        response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{file_size}'
    else:
        response = FileResponse(open(filepath, 'rb'), as_attachment=True)

    return response
