#!/bin/bash
# Render Deployment Guide for Clang AI Chatbot
# Execute this step by step

echo "🚀 RENDER DEPLOYMENT GUIDE - CLANG AI CHATBOT"
echo "==============================================="
echo ""

echo "📋 PREREQUISITES CHECK:"
echo "✅ GitHub repository: https://github.com/KrishnaRana238/clang_chatbot_ai"
echo "✅ render.yaml configuration file"
echo "✅ requirements.txt file"
echo "✅ Django settings configured for production"
echo ""

echo "🔐 STEP 1: CREATE RENDER ACCOUNT (if not already done)"
echo "1. Go to https://render.com"
echo "2. Sign up with your GitHub account"
echo "3. Authorize Render to access your repositories"
echo ""

echo "📱 STEP 2: DEPLOY VIA WEB INTERFACE (Recommended)"
echo "1. Go to https://dashboard.render.com"
echo "2. Click 'New +' button"
echo "3. Select 'Web Service'"
echo "4. Choose 'Build and deploy from a Git repository'"
echo "5. Connect your GitHub account if not connected"
echo "6. Select your repository: KrishnaRana238/clang_chatbot_ai"
echo "7. Configure the following settings:"
echo "   - Name: clang-ai-chatbot"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
echo "   - Start Command: gunicorn chatbot_project.wsgi:application --bind 0.0.0.0:\$PORT"
echo "8. Add Environment Variables:"
echo "   - DJANGO_SETTINGS_MODULE = chatbot_project.settings"
echo "   - DEBUG = False"
echo "   - ALLOWED_HOSTS = *"
echo "9. Click 'Create Web Service'"
echo ""

echo "🔧 STEP 3: ALTERNATIVE - RENDER CLI DEPLOYMENT"
echo "Note: Render CLI is limited, but here's the process:"
echo ""

echo "📦 Install Dependencies:"
echo "curl -fsSL https://cli.render.com/install | sh"
echo ""

echo "🔑 Login to Render:"
echo "render login"
echo ""

echo "🚀 Deploy:"
echo "render deploy"
echo ""

echo "⚙️  STEP 4: CONFIGURE ENVIRONMENT VARIABLES (if using CLI)"
echo "render env:set DJANGO_SETTINGS_MODULE=chatbot_project.settings"
echo "render env:set DEBUG=False"
echo "render env:set ALLOWED_HOSTS=*"
echo ""

echo "🔍 STEP 5: MONITOR DEPLOYMENT"
echo "1. Check deployment logs in Render dashboard"
echo "2. Verify the service is running"
echo "3. Test your application at the provided URL"
echo ""

echo "🌐 STEP 6: ACCESS YOUR DEPLOYED APP"
echo "Your app will be available at: https://clang-ai-chatbot.onrender.com"
echo "(URL may vary based on your service name)"
echo ""

echo "🐛 TROUBLESHOOTING:"
echo "- Check logs in Render dashboard for any errors"
echo "- Ensure all environment variables are set correctly"
echo "- Verify requirements.txt includes all dependencies"
echo "- Check that Django settings allow the Render domain"
echo ""

echo "✅ DEPLOYMENT COMPLETE!"
echo "Your Clang AI Chatbot should now be live on Render!"
