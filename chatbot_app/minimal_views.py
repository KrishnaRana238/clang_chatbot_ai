from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

def home(request):
    """Basic home page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clang AI Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; margin: 0 auto; text-align: center; }
            .status { background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Clang AI Chatbot</h1>
            <div class="status">
                <h2>✅ Deployment Successful!</h2>
                <p>Your chatbot is now live and ready for configuration.</p>
            </div>
            <p>Status: <strong>Online</strong></p>
            <p>Ready to add AI capabilities with your tokens.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def health(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Clang AI Chatbot is running',
        'deployment': 'minimal'
    })
