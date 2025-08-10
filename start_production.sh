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
echo "   Python Path: $(which python)"
echo "   Pip Path: $(which pip)"

# Upgrade pip first
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install all dependencies from requirements.txt
echo "📦 Installing all dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Verify critical imports
echo "� Verifying installations..."
python -c "import django; print(f'✅ Django {django.get_version()} is available')" || {
    echo "❌ Django import failed!"
    exit 1
}

python -c "import gunicorn; print('✅ Gunicorn is available')" || {
    echo "❌ Gunicorn import failed!"
    exit 1
}

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn server
echo "🌐 Starting Gunicorn server on port $PORT..."
exec python -m gunicorn chatbot_project.wsgi:application \
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
