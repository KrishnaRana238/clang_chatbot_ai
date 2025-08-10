#!/bin/bash
# Quick Render Deployment via API (Alternative to Web Interface)

echo "🔧 RENDER API DEPLOYMENT SCRIPT"
echo "================================"
echo ""

# Check if API key is provided
if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ Error: RENDER_API_KEY environment variable not set"
    echo "📋 To get your API key:"
    echo "1. Go to https://dashboard.render.com/account"
    echo "2. Navigate to 'API Keys' section"
    echo "3. Create a new API key"
    echo "4. Run: export RENDER_API_KEY='your-api-key-here'"
    echo ""
    exit 1
fi

echo "✅ API Key found. Proceeding with deployment..."

# Service configuration
SERVICE_NAME="clang-ai-chatbot"
REPO_URL="https://github.com/KrishnaRana238/clang_chatbot_ai"
BRANCH="main"

# Create service payload
cat > service_config.json << EOF
{
  "type": "web_service",
  "name": "$SERVICE_NAME",
  "repo": "$REPO_URL",
  "branch": "$BRANCH",
  "rootDir": ".",
  "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate",
  "startCommand": "gunicorn chatbot_project.wsgi:application --bind 0.0.0.0:\$PORT",
  "plan": "free",
  "region": "oregon",
  "envVars": [
    {
      "key": "DJANGO_SETTINGS_MODULE",
      "value": "chatbot_project.settings"
    },
    {
      "key": "DEBUG",
      "value": "False"
    },
    {
      "key": "ALLOWED_HOSTS",
      "value": "*"
    }
  ]
}
EOF

echo "📤 Creating service on Render..."

# Create the service
response=$(curl -s -X POST \
  "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d @service_config.json)

# Check if service was created successfully
if echo "$response" | grep -q '"id"'; then
    service_id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    service_url=$(echo "$response" | grep -o '"serviceDetails":{"url":"[^"]*"' | cut -d'"' -f6)
    
    echo "✅ Service created successfully!"
    echo "🆔 Service ID: $service_id"
    echo "🌐 Service URL: $service_url"
    echo ""
    echo "📊 Deployment Status:"
    echo "The deployment is now in progress. You can monitor it at:"
    echo "https://dashboard.render.com/web/$service_id"
    
else
    echo "❌ Failed to create service. Response:"
    echo "$response"
fi

# Cleanup
rm -f service_config.json

echo ""
echo "🔍 Next Steps:"
echo "1. Monitor deployment at https://dashboard.render.com"
echo "2. Check logs for any deployment issues"
echo "3. Test your application once deployment completes"
