#!/bin/bash

# Netlify build script
echo "Building Django chatbot for production..."

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create necessary directories
mkdir -p dist
mkdir -p .netlify/functions

# Copy templates to dist
cp -r templates/ dist/

echo "Build completed successfully!"
