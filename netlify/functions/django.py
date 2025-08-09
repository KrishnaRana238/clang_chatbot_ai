import json
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, '/opt/build/repo')

# Set Django settings before importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')

try:
    import django
    from django.conf import settings
    from django.core.wsgi import get_wsgi_application
    django.setup()
except ImportError:
    # Fallback if Django import fails
    pass

def handler(event, context):
    """
    Netlify function to handle Django backend requests
    """
    try:
        # Extract request information
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_string = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Remove /api prefix for Django routing
        if path.startswith('/api'):
            path = path[4:]
        
        # Create Django-compatible request
        environ = {
            'REQUEST_METHOD': http_method,
            'PATH_INFO': path,
            'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in query_string.items()]),
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)) if body else '0',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.input': body,
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add headers to environ
        for key, value in headers.items():
            key = key.upper().replace('-', '_')
            if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = f'HTTP_{key}'
            environ[key] = value
        
        # Get Django WSGI application
        application = get_wsgi_application()
        
        # Process request through Django
        response_data = []
        response_status = None
        response_headers = {}
        
        def start_response(status, headers, exc_info=None):
            nonlocal response_status, response_headers
            response_status = int(status.split(' ')[0])
            response_headers = dict(headers)
        
        # Get response from Django
        response_body = application(environ, start_response)
        response_content = b''.join(response_body).decode('utf-8')
        
        # Return Netlify function response
        return {
            'statusCode': response_status or 200,
            'headers': {
                'Content-Type': response_headers.get('Content-Type', 'application/json'),
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                **response_headers
            },
            'body': response_content
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }
