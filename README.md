# Clang AI Assistant - Advanced Multi-Provider Chatbot

🤖 **Clang** is a sophisticated AI assistant built with Django, featuring advanced LLM capabilities, multi-provider API integration, and intelligent question complexity analysis.

## 🚀 Key Features

### � **Advanced LLM Integration**
- **Question Complexity Analysis** - Automatically classifies and routes simple/medium/complex questions
- **RAG System** - Retrieval Augmented Generation with vector databases (FAISS/ChromaDB)
- **Multi-step Reasoning** - Enhanced prompting for complex interdisciplinary questions
- **Memory Management** - Conversation context with LangChain
- **Training Data Collection** - Continuous learning from interactions

### 🌐 **Multi-Provider API Support**
- **OpenRouter** - Access to GPT-4, Claude, and premium models
- **Cohere** - Command and Command-R-Plus models
- **Groq** - Lightning-fast inference with Llama models
- **Mistral AI** - European AI models
- **Together AI** - Open-source model hosting
- **Automatic Failover** - Seamless switching when rate limits are hit

### 🛠️ **Advanced Commands**
- `/analyze [question]` - Question complexity analysis
- `/training stats` - Performance and training statistics  
- `/feedback [rating] [comment]` - User feedback system
- `/knowledge add [text]` - Knowledge base expansion
- `/help` - Complete command reference

### 💻 **Technical Stack**
- **Backend**: Django 5.0.6 with REST API
- **AI Libraries**: LangChain, Transformers, Sentence-Transformers
- **Vector Storage**: FAISS, ChromaDB for semantic search
- **Frontend**: Chainlit UI + Custom HTML interface
- **Database**: SQLite with chat history and training data

## 📁 Project Structure

```
clang-chatbot-ai/
├── chatbot_project/              # Django project settings
│   ├── settings.py
│   ├── urls.py  
│   ├── wsgi.py
│   └── asgi.py
├── chatbot_app/                  # Main Django app
│   ├── models.py                 # Chat session and message models
│   ├── views.py                  # API endpoints
│   ├── serializers.py            # DRF serializers
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Admin interface
│   ├── chatbot_service.py        # Core chatbot logic with 5-provider API
│   └── advanced_llm_service.py   # Advanced LLM capabilities & RAG
├── templates/                    # HTML templates
│   └── chatbot_app/
│       └── index.html            # Web chat interface
├── knowledge_base/               # Vector database storage
├── training_data.jsonl          # Interaction logs for training
├── feedback_data.jsonl          # User feedback collection
├── chainlit_app.py               # Chainlit frontend application
├── requirements.txt              # All dependencies (74+ packages)
├── AI_SETUP_GUIDE.md            # Comprehensive setup guide
├── TRAINING_GUIDE.md            # Training and customization guide
├── manage.py                     # Django management
├── .env.example                  # Environment template
└── README.md                     # This file
```

## Setup Instructions

### 1. Environment Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd /Users/krishnarana/Desktop/Web\ Development/chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### 2. Environment Variables

1. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file and add your API keys:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DJANGO_SECRET_KEY=your_django_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   > **Note:** You can get an OpenAI API key from [OpenAI's website](https://platform.openai.com/api-keys)

### 3. Django Setup

1. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Applications

### Option 1: Django Web Interface

1. **Start the Django development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Web interface: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - API endpoints:
     - POST `/api/chat/` - Send a chat message
     - GET `/api/sessions/` - List all chat sessions
     - GET `/api/sessions/{session_id}/` - Get specific session

### Option 2: Chainlit Interface

1. **Start the Chainlit application**
## 🚀 Quick Start

### Option 1: Django Web Interface
```bash
python manage.py runserver
# Visit: http://127.0.0.1:8000/
```

### Option 2: Chainlit UI (Recommended)
```bash
chainlit run chainlit_app.py -w
# Visit: http://127.0.0.1:8000/
```

## 🧪 Advanced Features Demo

### Test Complex Question Analysis
```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "/analyze How does quantum computing impact modern cryptography and what are the implications for blockchain security?"}'
```

### Check Training Statistics
```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "/training stats"}'
```

### Add Feedback
```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "/feedback 5 Amazing AI assistant!"}'
```

## 🛠️ Development

### Run Tests
```bash
python manage.py test
python test_api_key.py
python test_openrouter.py
```

### View Admin Interface
```bash
python manage.py createsuperuser
python manage.py runserver
# Visit: http://127.0.0.1:8000/admin/
```

## 📊 Performance & Metrics

- **Question Processing**: 1-10 seconds based on complexity
- **Supported Models**: 50+ AI models across 5 providers
- **Context Memory**: 10 message conversation history
- **Vector Search**: Sub-second semantic retrieval
- **Training Data**: Continuous interaction logging

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** - Advanced LLM orchestration
- **OpenRouter** - Multi-model API access
- **Cohere** - Enterprise AI models
- **Chainlit** - Beautiful chat interface
- **Django** - Robust web framework
- **Open Source Community** - Continuous inspiration

## 🌟 Star History

If you find Clang useful, please give it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/clang-chatbot-ai&type=Timeline)](https://star-history.com/#YOUR_USERNAME/clang-chatbot-ai&Timeline)

## 📬 Support

- 🐛 [Report Issues](https://github.com/YOUR_USERNAME/clang-chatbot-ai/issues)
- 💡 [Feature Requests](https://github.com/YOUR_USERNAME/clang-chatbot-ai/issues/new?template=feature_request.md)
- 💬 [Discussions](https://github.com/YOUR_USERNAME/clang-chatbot-ai/discussions)

---

<div align="center">

**Built with ❤️ by AI enthusiasts**

[🌟 Star](https://github.com/YOUR_USERNAME/clang-chatbot-ai) • [🍴 Fork](https://github.com/YOUR_USERNAME/clang-chatbot-ai/fork) • [📋 Issues](https://github.com/YOUR_USERNAME/clang-chatbot-ai/issues) • [🚀 Deploy](GITHUB_SETUP.md)

</div>
Edit `chatbot_app/chatbot_service.py` to integrate different AI models or services.

### Customizing the UI
- Django: Edit `templates/chatbot_app/index.html`
- Chainlit: Modify `chainlit_app.py` and `.chainlit/config.toml`

### Database Configuration
Update `chatbot_project/settings.py` to use PostgreSQL or other databases for production.

## Troubleshooting

1. **OpenAI API Issues**: The app will fallback to simple responses if OpenAI is unavailable
2. **Port Conflicts**: Change ports using `--port` flag for Chainlit or `runserver 0.0.0.0:8080` for Django
3. **Migration Issues**: Run `python manage.py makemigrations chatbot_app` if needed

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up proper web server (nginx + gunicorn)
4. Use environment variables for sensitive data
5. Enable HTTPS

## License

This project is open source and available under the MIT License.
