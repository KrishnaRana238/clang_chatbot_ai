#!/bin/bash
# Production startup script for Render deployment

echo "🚀 Starting Clang AI Chatbot production server..."

# Set environment variables for production
export DJANGO_SETTINGS_MODULE=chatbot_project.settings
export DEBUG=False

# Ensure Python can find packages
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Print environment info
echo "📋 Environment Configuration:"
echo "   Django Settings: $DJANGO_SETTINGS_MODULE"
echo "   Debug Mode: $DEBUG"
echo "   Port: $PORT"
echo "   Python Path: $(which python)"
echo "   Working Directory: $(pwd)"

# Upgrade pip first
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip --no-cache-dir

# Install all dependencies from requirements.txt
echo "📦 Installing all dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt --no-cache-dir
    echo "📋 Installation completed. Checking what was installed..."
    python -m pip list | grep -E "(Django|gunicorn)"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Install critical packages individually if they failed
echo "🔧 Ensuring critical packages are installed..."
python -c "import django" 2>/dev/null || {
    echo "⚠️ Django not found, installing individually..."
    python -m pip install Django==4.2.7 --no-cache-dir
}

python -c "import gunicorn" 2>/dev/null || {
    echo "⚠️ Gunicorn not found, installing individually..."
    python -m pip install gunicorn==21.2.0 --no-cache-dir
}

# Verify critical imports
echo "🔍 Final verification..."
python -c "import django; print(f'✅ Django {django.get_version()} is available')" || {
    echo "❌ Django import failed even after individual installation!"
    echo "🔍 Python path: $(which python)"
    echo "🔍 Site packages: $(python -c 'import site; print(site.getsitepackages())')"
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
