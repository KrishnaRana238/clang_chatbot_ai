from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    """Ultra simple home page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clang AI Chatbot</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                max-width: 600px; 
                text-align: center;
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            .status { 
                background: rgba(46, 204, 113, 0.2); 
                padding: 20px; 
                border-radius: 12px; 
                margin: 20px 0;
                border: 1px solid rgba(46, 204, 113, 0.3);
            }
            h1 { font-size: 2.5em; margin-bottom: 20px; }
            .emoji { font-size: 3em; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🤖</div>
            <h1>Clang AI Chatbot</h1>
            <div class="status">
                <h2>✅ Deployment Successful!</h2>
                <p>Your chatbot is now live and ready for AI configuration.</p>
            </div>
            <p><strong>Status:</strong> Online & Ready</p>
            <p>Minimal deployment working perfectly!</p>
            <p>Ready to add AI capabilities with your tokens.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

@csrf_exempt
def health(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Clang AI Chatbot is running perfectly',
        'deployment': 'ultra-minimal',
        'ready_for_ai': True
    })
