# PostgreSQL Setup & Data Migration on Render

## 1. Add PostgreSQL Database in Render
- Go to Render dashboard → New → Database → PostgreSQL.
- Note your database name, user, password, host, and port.

## 2. Set Environment Variables in Render
- In your Render service settings, add:
	- POSTGRES_DB
	- POSTGRES_USER
	- POSTGRES_PASSWORD
	- POSTGRES_HOST
	- POSTGRES_PORT

## 3. Install PostgreSQL Driver
- Ensure `psycopg2-binary` is in your `requirements.txt`.

## 4. Migrate Django Data
- Push code changes to Render.
- On deploy, Django will run migrations automatically:
	```
	python manage.py migrate --noinput
	```

## 5. (Optional) Move Existing Data from SQLite to PostgreSQL
- Locally, run:
	```
	python manage.py dumpdata > data.json
	```
- Change your local `settings.py` to use PostgreSQL.
- Run migrations:
	```
	python manage.py migrate
	```
- Load data:
	```
	python manage.py loaddata data.json
	```

---
This will set up PostgreSQL and migrate your Django data for Render deployment.
# Enhanced Clang AI Assistant - Advanced Multi-Provider Chatbot with Emotional Intelligence

🤖 **Clang** is a sophisticated AI assistant built with Django multi-provider API integration, emotional intelligence, and human-like conversational abilities.

## 🚀 Key Features

### 🧠 **Emotional Intelligence & Human Chit-Chat**
- **Emotion Detection** - Recognizes happy, sad, angry, anxious, tired, confused states
- **Empathetic Responses** - Caring, supportive responses with appropriate emojis
- **Social Awareness** - Natural greetings, check-ins, and casual conversations
- **Life Situation Support** - Understanding responses to relationship, work, family issues
- **Time-Sensitive Greetings** - Morning, afternoon, evening, and bedtime interactions

### 🏥 **Advanced Medical Expertise**
- **Comprehensive Database** - 10+ medical conditions, 6+ medications
- **Emergency Detection** - Identifies urgent medical situations
- **Drug Interaction Checker** - Professional safety analysis
- **Symptom Analysis** - Detailed condition matching with urgency levels
- **Safety Protocols** - Proper medical disclaimers and professional consultation recommendations

### ✍️ **Academic Essay Writing**
- **12+ Topic Categories** - Technology, environment, education, health, etc.
- **200-Word Optimization** - Precisely crafted essays within word limits
- **Smart Categorization** - Automatic essay type and structure detection
- **Quality Content** - Well-structured, informative academic writing

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



## 🙏 Acknowledgments

- **OpenRouter** - Multi-model API access
- **Cohere** - Enterprise AI models
- **Chainlit** - Beautiful chat interface
- **Django** - Robust web framework
- **Open Source Community** - Continuous inspiration


**Built with ❤️ by AI enthusiasts**

[🌟 Star](https://github.com/YOUR_USERNAME/clang-chatbot-ai) • [🍴 Fork](https://github.com/YOUR_USERNAME/clang-chatbot-ai/fork) • [📋 Issues](https://github.com/YOUR_USERNAME/clang-chatbot-ai/issues) • [🚀 Deploy](GITHUB_SETUP.md)

## License

This project is open source and available under the MIT License.
