#!/bin/bash
# Production startup script for Render deployment

echo "🚀 Starting Clang AI Chatbot production server..."

# Set environment variables for production
export DJANGO_SETTINGS_MODULE=chatbot_project.settings
export DEBUG=False

# Print environment info
echo "📋 Environment Configuration:"
echo "   Django Settings: $DJANGO_SETTINGS_MODULE"
echo "   Debug Mode: $DEBUG"
echo "   Port: $PORT"

# Check if gunicorn is available
if ! command -v gunicorn &> /dev/null; then
    echo "❌ Error: gunicorn not found. Installing..."
    pip install gunicorn
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import django, requests, gunicorn" 2>/dev/null || {
    echo "⚠️  Installing missing dependencies..."
    pip install -r requirements.txt
}

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn server
echo "🌐 Starting Gunicorn server on port $PORT..."
exec gunicorn chatbot_project.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
