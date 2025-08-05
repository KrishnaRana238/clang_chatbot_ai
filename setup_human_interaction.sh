#!/bin/bash

echo "🚀 Setting up Human Interaction Optimization for Clang AI"
echo "=================================================="

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install spacy>=3.4.0 nltk>=3.7 textblob>=0.17.1

# Download spaCy English model
echo "🧠 Downloading spaCy English language model..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
print('✅ NLTK data downloaded')
"

# Create database
echo "🗄️ Initializing conversation memory database..."
python -c "
from chatbot_app.conversation_memory import ConversationMemory
memory = ConversationMemory()
print('✅ Database initialized')
"

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Run the training script: python train_human_interaction.py"
echo "2. Test your optimized chatbot with human-like interactions"
echo "3. Collect user feedback to improve further"
