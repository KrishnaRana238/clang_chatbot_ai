#!/bin/bash

# Quick Setup Script for Open-Source Chatbot
echo "🚀 Setting up Open-Source Chatbot..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Please activate your virtual environment first:"
    echo "   source venv/bin/activate"
    exit 1
fi

echo "📦 Installing basic dependencies..."
pip install -r requirements-lite.txt

echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
else
    echo "⚠️  .env file already exists"
fi

echo "🗄️ Setting up database..."
python3 manage.py makemigrations chatbot_app
python3 manage.py migrate

echo "✅ Setup complete!"
echo ""
echo "🎯 To run the chatbot:"
echo "   Option 1 - Django only:     python3 manage.py runserver"
echo "   Option 2 - Chainlit only:   chainlit run chainlit_app.py -w"
echo ""
echo "🔧 To install AI models (optional, takes longer):"
echo "   pip install transformers torch accelerate sentencepiece"
echo ""
echo "🚀 Ready to chat!"
