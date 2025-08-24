#!/bin/bash

# Minimal build script for fast deployment
set -o errexit

echo "🚀 Starting minimal deployment..."

# Install only essential packages
pip install --upgrade pip
pip install -r requirements-basic.txt

echo "✅ Dependencies installed"

# Create basic static files directory
mkdir -p staticfiles
echo "/* Static files */" > staticfiles/style.css

echo "✅ Static files ready"
echo "🎉 Build completed successfully"
