

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Import LangChain components
from langchain.memory import ConversationBufferWindowMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.document_loaders import TextLoader

# Import transformers for local models
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

load_dotenv()

class AdvancedLLMService:
    """Advanced LLM service for complex question handling and training capabilities"""
    
    def __init__(self, existing_chatbot_service=None):
        self.existing_service = existing_chatbot_service
        self.setup_components()
        self.setup_knowledge_base()
        self.setup_training_data()
        
    def setup_components(self):
        """Initialize all LLM components"""
        # Memory for conversation context
        self.memory = ConversationBufferWindowMemory(
            k=10,  # Remember last 10 exchanges
            return_messages=True
        )
        
        # Text splitter for document processing
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Embeddings model for semantic search
        try:
            # Try OpenAI embeddings first (requires API key)
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv('OPENROUTER_API_KEY', os.getenv('OPENAI_API_KEY'))
            )
            print("✅ Using OpenAI embeddings")
        except:
            try:
                # Fallback to local sentence transformers
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✅ Using local sentence transformers embeddings")
            except:
                print("❌ Could not load embeddings model")
                self.embeddings = None
                self.sentence_model = None
        
        # Complexity analyzer
        self.setup_complexity_analyzer()
        
        print("✅ Advanced LLM components initialized")

    def setup_complexity_analyzer(self):
        """Setup question complexity analysis"""
        self.complexity_indicators = {
            'simple': [
                'what is', 'who is', 'when', 'where', 'yes', 'no',
                'define', 'meaning', 'explain simply'
            ],
            'medium': [
                'how to', 'why', 'compare', 'difference', 'analyze',
                'explain', 'describe', 'summarize'
            ],
            'complex': [
                'evaluate', 'synthesize', 'critique', 'justify', 'argue',
                'design', 'create', 'solve', 'optimize', 'predict',
                'multistep', 'research', 'comprehensive'
            ]
        }
        
    def setup_knowledge_base(self):
        """Initialize vector database for knowledge storage"""
        self.knowledge_base_path = "knowledge_base"
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        
        # Initialize vector stores
        try:
            if self.embeddings:
                # Use FAISS for fast similarity search
                self.vector_store = None  # Will be created when documents are added
                print("✅ Vector store ready (FAISS)")
            else:
                print("⚠️  Vector store unavailable (no embeddings)")
        except Exception as e:
            print(f"⚠️  Vector store setup failed: {e}")

    def setup_training_data(self):
        """Initialize training data collection"""
        self.training_data_file = "training_data.jsonl"
        self.feedback_data = []
        
        # Create training data file if it doesn't exist
        if not os.path.exists(self.training_data_file):
            with open(self.training_data_file, 'w') as f:
                pass
        
        print("✅ Training data collection ready")

    def analyze_question_complexity(self, question: str) -> Dict[str, Any]:
        """Analyze question complexity and recommend appropriate handling"""
        question_lower = question.lower()
        
        # Count complexity indicators
        simple_count = sum(1 for indicator in self.complexity_indicators['simple'] 
                          if indicator in question_lower)
        medium_count = sum(1 for indicator in self.complexity_indicators['medium'] 
                          if indicator in question_lower)
        complex_count = sum(1 for indicator in self.complexity_indicators['complex'] 
                           if indicator in question_lower)
        
        # Additional complexity factors
        word_count = len(question.split())
        has_multiple_questions = '?' in question[:-1]  # Multiple question marks
        has_technical_terms = any(term in question_lower for term in [
            'algorithm', 'machine learning', 'artificial intelligence', 'neural network',
            'optimization', 'statistical', 'mathematical', 'scientific'
        ])
        
        # Determine complexity level
        if complex_count > 0 or word_count > 30 or has_multiple_questions or has_technical_terms:
            complexity = 'complex'
            confidence = 0.8 + min(complex_count * 0.1, 0.2)
        elif medium_count > simple_count or word_count > 15:
            complexity = 'medium'
            confidence = 0.6 + min(medium_count * 0.1, 0.3)
        else:
            complexity = 'simple'
            confidence = 0.5 + min(simple_count * 0.1, 0.4)
        
        return {
            'complexity': complexity,
            'confidence': min(confidence, 1.0),
            'word_count': word_count,
            'requires_rag': complexity in ['medium', 'complex'],
            'requires_chain_of_thought': complexity == 'complex',
            'estimated_processing_time': {
                'simple': '1-2 seconds',
                'medium': '3-5 seconds', 
                'complex': '5-10 seconds'
            }[complexity]
        }

    async def add_knowledge_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the knowledge base"""
        if not self.embeddings:
            print("⚠️  Cannot add documents: embeddings not available")
            return False
            
        try:
            # Process documents
            all_docs = []
            for i, doc_content in enumerate(documents):
                chunks = self.text_splitter.split_text(doc_content)
                for chunk in chunks:
                    doc_metadata = metadata[i] if metadata and i < len(metadata) else {}
                    all_docs.append(Document(page_content=chunk, metadata=doc_metadata))
            
            # Create or update vector store
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(all_docs, self.embeddings)
            else:
                self.vector_store.add_documents(all_docs)
            
            # Save vector store
            self.vector_store.save_local(f"{self.knowledge_base_path}/faiss_index")
            print(f"✅ Added {len(all_docs)} document chunks to knowledge base")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add documents: {e}")
            return False

    async def retrieve_relevant_context(self, question: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant context from knowledge base"""
        if not self.vector_store:
            return []
        
        try:
            # Perform similarity search
            results = self.vector_store.similarity_search_with_score(question, k=top_k)
            
            context_docs = []
            for doc, score in results:
                context_docs.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'relevance_score': 1 - score  # Convert distance to similarity
                })
            
            return context_docs
            
        except Exception as e:
            print(f"❌ Context retrieval failed: {e}")
            return []

    async def generate_enhanced_response(self, question: str, conversation_history: List = None) -> Dict[str, Any]:
        """Generate enhanced response using complexity analysis and RAG"""
        
        # Analyze question complexity
        complexity_analysis = self.analyze_question_complexity(question)
        
        # Start response metadata
        response_metadata = {
            'complexity_analysis': complexity_analysis,
            'processing_steps': [],
            'sources_used': [],
            'confidence': 0.0
        }
        
        response_metadata['processing_steps'].append('Question complexity analyzed')
        
        # Retrieve context if needed
        context_docs = []
        if complexity_analysis['requires_rag']:
            context_docs = await self.retrieve_relevant_context(question)
            response_metadata['processing_steps'].append('Relevant context retrieved')
            response_metadata['sources_used'] = [doc['metadata'] for doc in context_docs]
        
        # Prepare enhanced prompt
        enhanced_prompt = self.create_enhanced_prompt(
            question, 
            context_docs, 
            complexity_analysis,
            conversation_history
        )
        
        response_metadata['processing_steps'].append('Enhanced prompt created')
        
        # Get response from existing chatbot service
        if self.existing_service:
            try:
                # Use the existing multi-API system
                raw_response = await self.existing_service._get_multi_api_response(
                    enhanced_prompt, conversation_history
                )
                response_metadata['processing_steps'].append('Response generated via existing API')
                response_metadata['confidence'] = 0.85
                
            except Exception as e:
                print(f"❌ API call failed: {e}")
                raw_response = "I apologize, but I'm having trouble generating a response right now."
                response_metadata['confidence'] = 0.1
        else:
            raw_response = self.generate_local_response(enhanced_prompt)
            response_metadata['processing_steps'].append('Response generated locally')
            response_metadata['confidence'] = 0.7
        
        # Post-process response
        final_response = self.post_process_response(
            raw_response, 
            complexity_analysis, 
            context_docs
        )
        
        response_metadata['processing_steps'].append('Response post-processed')
        
        # Log for training
        await self.log_interaction(question, final_response, response_metadata)
        
        return {
            'response': final_response,
            'metadata': response_metadata,
            'complexity': complexity_analysis['complexity'],
            'sources': len(context_docs)
        }

    def create_enhanced_prompt(self, question: str, context_docs: List, complexity: Dict, history: List = None) -> str:
        """Create an enhanced prompt based on complexity and available context"""
        
        # Base prompt template
        if complexity['complexity'] == 'complex':
            system_prompt = """You are an advanced AI assistant capable of handling complex, multi-faceted questions. 
            Use step-by-step reasoning, consider multiple perspectives, and provide comprehensive answers.
            When given context information, integrate it naturally into your response."""
            
        elif complexity['complexity'] == 'medium':
            system_prompt = """You are a knowledgeable AI assistant. Provide detailed, well-structured answers 
            that address all aspects of the question. Use provided context to enhance your response."""
            
        else:  # simple
            system_prompt = """You are a helpful AI assistant. Provide clear, concise, and direct answers.
            Keep your response focused and easy to understand."""
        
        # Add context if available
        context_section = ""
        if context_docs:
            context_section = "\n\n**Relevant Context:**\n"
            for i, doc in enumerate(context_docs[:3], 1):
                context_section += f"{i}. {doc['content']}\n"
        
        # Add conversation history
        history_section = ""
        if history and len(history) > 0:
            history_section = "\n\n**Previous Context:**\n"
            for msg in history[-3:]:  # Last 3 messages
                role = "User" if msg.get("message_type") == "user" else "Assistant"
                content = msg.get("content", "")[:200] + "..." if len(msg.get("content", "")) > 200 else msg.get("content", "")
                history_section += f"{role}: {content}\n"
        
        # Chain of thought for complex questions
        thinking_instruction = ""
        if complexity['requires_chain_of_thought']:
            thinking_instruction = "\n\nThink through this step-by-step before providing your final answer."
        
        enhanced_prompt = f"""{system_prompt}{context_section}{history_section}{thinking_instruction}

**Question:** {question}

Please provide a helpful and accurate response."""
        
        return enhanced_prompt

    def post_process_response(self, response: str, complexity: Dict, context_docs: List) -> str:
        """Post-process the response based on complexity and context"""
        
        # Add complexity indicator
        if complexity['complexity'] == 'complex':
            prefix = "🧠 **Complex Analysis:** "
        elif complexity['complexity'] == 'medium':
            prefix = "🔍 **Detailed Response:** "
        else:
            prefix = "💡 **Quick Answer:** "
        
        # Add source attribution if context was used
        suffix = ""
        if context_docs:
            suffix = f"\n\n*Response enhanced with {len(context_docs)} relevant sources*"
        
        return f"{prefix}{response}{suffix}"

    def generate_local_response(self, prompt: str) -> str:
        """Generate response using local models if available"""
        if not HAS_TRANSFORMERS:
            return "I need additional API access to provide a comprehensive response to this question."
        
        try:
            # Use a simple local pipeline for demonstration
            # In production, you'd use more sophisticated local models
            return f"I understand your question: '{prompt[:100]}...'. This appears to be a complex query that would benefit from additional context and processing capabilities."
        except Exception as e:
            return f"I'm having trouble processing this question locally. Error: {str(e)}"

    async def log_interaction(self, question: str, response: str, metadata: Dict):
        """Log interaction for training data collection"""
        try:
            interaction_log = {
                'timestamp': asyncio.get_event_loop().time(),
                'question': question,
                'response': response,
                'metadata': metadata
            }
            
            # Append to training data file
            with open(self.training_data_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(interaction_log, ensure_ascii=False) + '\n')
                
        except Exception as e:
            print(f"⚠️  Failed to log interaction: {e}")

    async def add_feedback(self, question: str, response: str, feedback_score: float, feedback_text: str = ""):
        """Add user feedback for training improvement"""
        feedback_entry = {
            'timestamp': asyncio.get_event_loop().time(),
            'question': question,
            'response': response,
            'feedback_score': feedback_score,  # 1-5 scale
            'feedback_text': feedback_text
        }
        
        self.feedback_data.append(feedback_entry)
        
        # Save feedback to file
        feedback_file = "feedback_data.jsonl"
        try:
            with open(feedback_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(feedback_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️  Failed to save feedback: {e}")

    def get_training_statistics(self) -> Dict[str, Any]:
        """Get statistics about training data and system performance"""
        try:
            # Count training interactions
            interaction_count = 0
            complexity_counts = {'simple': 0, 'medium': 0, 'complex': 0}
            
            if os.path.exists(self.training_data_file):
                with open(self.training_data_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            interaction_count += 1
                            try:
                                data = json.loads(line)
                                complexity = data.get('metadata', {}).get('complexity_analysis', {}).get('complexity', 'simple')
                                complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
                            except:
                                pass
            
            # Count feedback entries
            feedback_count = len(self.feedback_data)
            
            # Vector store stats
            vector_store_docs = 0
            if self.vector_store:
                try:
                    vector_store_docs = len(self.vector_store.docstore._dict)
                except:
                    vector_store_docs = "Unknown"
            
            return {
                'total_interactions': interaction_count,
                'complexity_distribution': complexity_counts,
                'feedback_entries': feedback_count,
                'knowledge_base_documents': vector_store_docs,
                'embeddings_available': self.embeddings is not None,
                'local_models_available': HAS_TRANSFORMERS
            }
            
        except Exception as e:
            return {'error': f"Failed to get statistics: {e}"}

    async def suggest_training_improvements(self) -> List[str]:
        """Analyze training data and suggest improvements"""
        suggestions = []
        
        stats = self.get_training_statistics()
        
        # Check interaction volume
        if stats.get('total_interactions', 0) < 100:
            suggestions.append("💡 Collect more training interactions (current: {}) to improve model performance".format(stats.get('total_interactions', 0)))
        
        # Check complexity distribution
        complexity_dist = stats.get('complexity_distribution', {})
        if complexity_dist.get('complex', 0) < 10:
            suggestions.append("🧠 Add more complex questions to improve handling of difficult queries")
        
        # Check feedback
        if stats.get('feedback_entries', 0) < 20:
            suggestions.append("📝 Collect more user feedback to identify areas for improvement")
        
        # Check knowledge base
        if stats.get('knowledge_base_documents', 0) == 0:
            suggestions.append("📚 Add domain-specific documents to the knowledge base for better context")
        
        if not stats.get('embeddings_available', False):
            suggestions.append("🔧 Configure embeddings (OpenAI API key) for better semantic search capabilities")
        
        return suggestions

# Integration function to connect with existing chatbot
def integrate_with_existing_chatbot(existing_chatbot_service):
    """Create and integrate advanced LLM service with existing chatbot"""
    advanced_service = AdvancedLLMService(existing_chatbot_service)
    
    # Add method to existing service for advanced processing
    existing_chatbot_service.advanced_llm = advanced_service
    existing_chatbot_service.handle_complex_question = advanced_service.generate_enhanced_response
    
    print("✅ Advanced LLM service integrated with existing chatbot")
    return advanced_service
