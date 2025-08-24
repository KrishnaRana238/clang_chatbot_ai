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
    python -m pip install -r requirements.txt --no-cache-dir --force-reinstall
    echo "📋 Installation completed. Checking what was installed..."
    python -m pip list | grep -E "(Django|gunicorn|dotenv|requests)"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Install critical packages individually if they failed
echo "🔧 Ensuring ALL critical packages are installed..."
python -c "import django" 2>/dev/null || {
    echo "⚠️ Django not found, installing individually..."
    python -m pip install Django==4.2.7 --no-cache-dir
}

python -c "import gunicorn" 2>/dev/null || {
    echo "⚠️ Gunicorn not found, installing individually..."
    python -m pip install gunicorn==21.2.0 --no-cache-dir
}

python -c "from dotenv import load_dotenv" 2>/dev/null || {
    echo "⚠️ python-dotenv not found, installing individually..."
    python -m pip install python-dotenv==1.0.0 --no-cache-dir
}

python -c "import requests" 2>/dev/null || {
    echo "⚠️ requests not found, installing individually..."
    python -m pip install requests==2.31.0 --no-cache-dir
}

# Install ALL packages from requirements.txt individually as backup
echo "🔧 Installing all requirements individually as backup..."
python -m pip install whitenoise==6.6.0 --no-cache-dir
python -m pip install psycopg2-binary==2.9.9 --no-cache-dir
python -m pip install django-cors-headers==4.3.1 --no-cache-dir
python -m pip install django-extensions==3.2.3 --no-cache-dir
python -m pip install djangorestframework==3.14.0 --no-cache-dir

# Verify critical imports
echo "🔍 Final verification of all critical imports..."
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

python -c "from dotenv import load_dotenv; print('✅ python-dotenv is available')" || {
    echo "❌ python-dotenv import failed!"
    exit 1
}

python -c "import requests; print('✅ requests is available')" || {
    echo "❌ requests import failed!"
    exit 1
}

python -c "import whitenoise; print('✅ whitenoise is available')" || {
    echo "⚠️ whitenoise import failed (non-critical)"
}

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn server
echo "🌐 DEBUG: About to start Gunicorn server on port $PORT..."
ls -l
env
exec python -m gunicorn chatbot_project.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 1 \
    --worker-class sync \
    --worker-connections 100 \
    --max-requests 100 \
    --max-requests-jitter 50 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
