"""
Enhanced Clang AI Chatbot Service with Advanced Knowledge Base Integration
Comprehensive AI assistant with NLP, knowledge base, math, and grammar capabilities
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Import our enhanced services
try:
    from .knowledge_base_service import (
        knowledge_base, grammar_checker, math_calculator, get_knowledge_response
    )
    from .nlp_processor import nlp_processor, process_user_query
    from .chatbot_service import OpenSourceChatbotService
    HAS_ENHANCED_SERVICES = True
except ImportError as e:
    print(f"⚠️  Enhanced services not available: {e}")
    HAS_ENHANCED_SERVICES = False
    try:
        from .chatbot_service import OpenSourceChatbotService
    except ImportError:
        print("❌ Basic chatbot service not available")

class EnhancedClangChatbot:
    """
    Advanced Clang AI Chatbot with comprehensive capabilities:
    - Multi-domain knowledge base
    - Advanced NLP processing
    - Grammar checking and correction
    - Mathematical problem solving
    - Code generation and debugging
    - Conversational AI with context awareness
    """
    
    def __init__(self):
        self.name = "Clang"
        self.version = "2.0 Advanced"
        self.capabilities = {
            'knowledge_base': True,
            'nlp_processing': True,
            'grammar_checking': True,
            'math_solving': True,
            'code_generation': True,
            'paraphrasing': True,
            'multi_language': False,  # Future enhancement
            'voice_interaction': False  # Future enhancement
        }
        
        # Initialize base chatbot service
        try:
            self.base_chatbot = OpenSourceChatbotService()
            print(f"✅ {self.name} {self.version} initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize base chatbot: {e}")
            self.base_chatbot = None
        
        # Track conversation context
        self.conversation_memory = []
        self.user_preferences = {}
        self.session_stats = {
            'queries_processed': 0,
            'knowledge_searches': 0,
            'math_problems_solved': 0,
            'grammar_checks': 0,
            'code_requests': 0,
            'session_start': datetime.now()
        }
    
    async def get_enhanced_response(self, user_message: str, conversation_history: List = None) -> Dict[str, Any]:
        """
        Main method to process user queries with full AI capabilities
        Returns comprehensive response with metadata
        """
        
        start_time = datetime.now()
        self.session_stats['queries_processed'] += 1
        
        try:
            # Step 1: Advanced NLP Analysis
            if HAS_ENHANCED_SERVICES:
                nlp_analysis = await process_user_query(user_message)
                analysis = nlp_analysis['analysis']
                response_strategy = nlp_analysis['response_strategy']
            else:
                # Fallback to basic analysis
                analysis = None
                response_strategy = {'should_search_knowledge': True, 'complexity_level': 'medium'}
            
            # Step 2: Route to appropriate handler based on intent
            response_data = await self._route_query(user_message, analysis, response_strategy, conversation_history)
            
            # Step 3: Enhance response with context and personality
            final_response = self._enhance_response_with_personality(response_data, analysis)
            
            # Step 4: Update conversation memory
            self._update_conversation_memory(user_message, final_response, analysis)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'response': final_response,
                'metadata': {
                    'processing_time_seconds': processing_time,
                    'intent': analysis.intent if analysis else 'unknown',
                    'confidence': analysis.confidence if analysis else 0.5,
                    'complexity': response_strategy.get('complexity_level', 'medium'),
                    'sources_used': response_data.get('sources', []),
                    'capabilities_activated': response_data.get('capabilities', []),
                    'session_stats': self.session_stats.copy()
                },
                'conversation_context': {
                    'memory_items': len(self.conversation_memory),
                    'user_preferences': self.user_preferences,
                    'suggested_followup': self._generate_followup_suggestions(analysis, response_data)
                }
            }
            
        except Exception as e:
            return {
                'response': f"I encountered an issue while processing your request: {str(e)}. Let me try to help you in a simpler way.",
                'metadata': {
                    'error': str(e),
                    'processing_time_seconds': (datetime.now() - start_time).total_seconds(),
                    'fallback_used': True
                },
                'conversation_context': {}
            }
    
    async def _route_query(self, query: str, analysis, strategy: Dict, history: List) -> Dict[str, Any]:
        """Route query to appropriate processing pipeline"""
        
        sources_used = []
        capabilities_activated = []
        
        # Handle mathematical queries
        if strategy.get('should_calculate', False):
            self.session_stats['math_problems_solved'] += 1
            capabilities_activated.append('mathematical_solver')
            
            if HAS_ENHANCED_SERVICES:
                math_result = math_calculator.solve_equation(query)
                if math_result['type'] != 'error':
                    sources_used.append('sympy_calculator')
                    return {
                        'response': f"**🔢 Mathematical Solution**\n\n**Problem:** {query}\n\n**Answer:** {math_result['result']}\n\n**Steps:**\n" + "\n".join([f"• {step}" for step in math_result['steps']]),
                        'sources': sources_used,
                        'capabilities': capabilities_activated,
                        'type': 'math_solution'
                    }
        
        # Handle grammar checking
        if strategy.get('should_check_grammar', False):
            self.session_stats['grammar_checks'] += 1
            capabilities_activated.append('grammar_checker')
            
            if HAS_ENHANCED_SERVICES:
                # Extract text to check (simple heuristic)
                text_to_check = query.replace('check grammar', '').replace('correct this', '').strip(' ":')
                grammar_result = grammar_checker.check_grammar(text_to_check)
                sources_used.append('textblob_grammar')
                
                response = f"**✍️ Grammar Check Results**\n\n"
                response += f"**Original:** {grammar_result['original']}\n\n"
                
                if grammar_result['original'] != grammar_result['corrected']:
                    response += f"**Corrected:** {grammar_result['corrected']}\n\n"
                else:
                    response += f"**Status:** Your grammar looks good! ✅\n\n"
                
                if grammar_result['suggestions']:
                    response += f"**Suggestions:**\n" + "\n".join([f"• {s}" for s in grammar_result['suggestions']])
                
                return {
                    'response': response,
                    'sources': sources_used,
                    'capabilities': capabilities_activated,
                    'type': 'grammar_check'
                }
        
        # Handle paraphrasing requests
        if strategy.get('should_paraphrase', False):
            capabilities_activated.append('text_paraphraser')
            
            if HAS_ENHANCED_SERVICES:
                # Extract text to paraphrase
                text_to_paraphrase = query.replace('paraphrase', '').replace('rephrase', '').strip(' ":')
                paraphrase_result = await nlp_processor.paraphrase_text(text_to_paraphrase)
                sources_used.append('textblob_paraphraser')
                
                response = f"**📝 Paraphrasing Results**\n\n"
                response += f"**Original:** {paraphrase_result.original}\n\n"
                response += f"**Alternatives:**\n"
                
                for i, alt in enumerate(paraphrase_result.paraphrases[:3], 1):
                    response += f"{i}. {alt}\n"
                
                if paraphrase_result.style_variations:
                    response += f"\n**Style Variations:**\n"
                    for i, var in enumerate(paraphrase_result.style_variations, 1):
                        response += f"{i}. {var}\n"
                
                return {
                    'response': response,
                    'sources': sources_used,
                    'capabilities': capabilities_activated,
                    'type': 'paraphrasing'
                }
        
        # Handle coding requests
        if strategy.get('should_provide_code', False):
            self.session_stats['code_requests'] += 1
            capabilities_activated.append('code_generator')
            
            # Use base chatbot for code generation (it has good coding knowledge)
            if self.base_chatbot:
                code_response = await self.base_chatbot.get_response(query, history)
                sources_used.append('multi_api_llm')
                return {
                    'response': f"**💻 Code Solution**\n\n{code_response}",
                    'sources': sources_used,
                    'capabilities': capabilities_activated,
                    'type': 'code_generation'
                }
        
        # Handle knowledge base queries
        if strategy.get('should_search_knowledge', False) or 'explain' in query.lower() or '?' in query:
            self.session_stats['knowledge_searches'] += 1
            capabilities_activated.append('knowledge_base')
            
            if HAS_ENHANCED_SERVICES:
                # Search comprehensive knowledge base
                knowledge_response = get_knowledge_response(query)
                sources_used.append('clang_knowledge_base')
                
                # If knowledge base has good info, return it
                if "don't have specific information" not in knowledge_response:
                    return {
                        'response': f"**🧠 Knowledge Base Response**\n\n{knowledge_response}",
                        'sources': sources_used,
                        'capabilities': capabilities_activated,
                        'type': 'knowledge_query'
                    }
        
        # Default: Use advanced LLM for general conversation
        if self.base_chatbot:
            capabilities_activated.append('conversational_ai')
            llm_response = await self.base_chatbot.get_response(query, history)
            sources_used.append('multi_api_llm')
            
            return {
                'response': llm_response,
                'sources': sources_used,
                'capabilities': capabilities_activated,
                'type': 'general_conversation'
            }
        else:
            # Absolute fallback
            return {
                'response': "I'm experiencing some technical difficulties, but I'm here to help! Could you please rephrase your question?",
                'sources': ['fallback'],
                'capabilities': ['basic_response'],
                'type': 'fallback'
            }
    
    def _enhance_response_with_personality(self, response_data: Dict, analysis) -> str:
        """Add Clang's personality and helpful context to responses"""
        
        base_response = response_data['response']
        response_type = response_data.get('type', 'general')
        
        # Add personality based on response type
        personality_intros = {
            'math_solution': "I love solving mathematical problems! 🔢 ",
            'grammar_check': "As your writing assistant, ",
            'code_generation': "Here's a coding solution for you! 💻 ",
            'knowledge_query': "Let me share what I know about this topic! 📚 ",
            'paraphrasing': "I can help you express this in different ways! ✍️ "
        }
        
        intro = personality_intros.get(response_type, "")
        
        # Add helpful context
        if response_type == 'math_solution':
            outro = "\n\n💡 **Tip:** I can solve equations, calculate derivatives, integrals, and more! Just ask me any math question."
        elif response_type == 'grammar_check':
            outro = "\n\n💡 **Tip:** I can also help with paraphrasing, style improvements, and writing suggestions!"
        elif response_type == 'knowledge_query':
            outro = "\n\n💡 **Tip:** I have knowledge in coding, history, geography, politics, writing, math, and science. Feel free to explore!"
        else:
            outro = ""
        
        # Combine with personality
        enhanced_response = intro + base_response + outro
        
        return enhanced_response
    
    def _update_conversation_memory(self, user_message: str, response: str, analysis):
        """Update conversation memory for context awareness"""
        
        memory_item = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'response_preview': response[:200] + "..." if len(response) > 200 else response,
            'intent': analysis.intent if analysis else 'unknown',
            'complexity': analysis.complexity_score if analysis else 0.5
        }
        
        self.conversation_memory.append(memory_item)
        
        # Keep only last 10 interactions to manage memory
        if len(self.conversation_memory) > 10:
            self.conversation_memory = self.conversation_memory[-10:]
    
    def _generate_followup_suggestions(self, analysis, response_data: Dict) -> List[str]:
        """Generate contextual follow-up suggestions"""
        
        suggestions = []
        response_type = response_data.get('type', 'general')
        
        if response_type == 'math_solution':
            suggestions = [
                "Would you like me to explain any of these steps?",
                "Can I help you with a related math problem?",
                "Would you like to see a graph of this equation?"
            ]
        elif response_type == 'knowledge_query':
            suggestions = [
                "Would you like more details on any specific aspect?",
                "Can I explain any related concepts?",
                "Would you like examples or practical applications?"
            ]
        elif response_type == 'code_generation':
            suggestions = [
                "Would you like me to explain how this code works?",
                "Can I help optimize or improve this code?",
                "Would you like to see alternative approaches?"
            ]
        else:
            suggestions = [
                "Is there anything specific you'd like me to clarify?",
                "Would you like to explore related topics?",
                "Can I help you with something else?"
            ]
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def get_capabilities_info(self) -> Dict[str, Any]:
        """Return information about Clang's capabilities"""
        
        return {
            'name': self.name,
            'version': self.version,
            'core_capabilities': {
                '🧠 Knowledge Base': 'Comprehensive knowledge in coding, history, geography, politics, writing, math, and science',
                '💻 Programming Help': 'Code generation, debugging, and programming concept explanations',
                '🔢 Mathematics': 'Equation solving, calculus, algebra, and mathematical problem solving',
                '✍️ Writing Assistant': 'Grammar checking, style improvement, and paraphrasing',
                '🤖 Conversational AI': 'Natural language understanding and intelligent responses',
                '🎯 Intent Recognition': 'Advanced understanding of user queries and context'
            },
            'supported_topics': {
                'Programming': ['Python', 'JavaScript', 'C++', 'Java', 'Web Development', 'Algorithms', 'Data Structures'],
                'Mathematics': ['Algebra', 'Calculus', 'Geometry', 'Statistics', 'Mathematical Proofs'],
                'History': ['World History', 'Ancient Civilizations', 'Modern History', 'Cultural Heritage'],
                'Geography': ['World Countries', 'Cities', 'Landmarks', 'Cultural Insights'],
                'Writing': ['Grammar Rules', 'Style Guides', 'Essay Writing', 'Creative Writing'],
                'Science': ['Physics', 'Chemistry', 'Biology', 'Computer Science']
            },
            'session_statistics': self.session_stats,
            'enhanced_features': list(self.capabilities.keys())
        }

    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        import uuid
        return str(uuid.uuid4())

    def format_conversation_history(self, messages) -> list:
        """Format conversation history for the enhanced chatbot"""
        conversation = []
        for message in messages:
            role = "user" if message.message_type == "user" else "assistant"
            conversation.append({
                "role": role,
                "content": message.content
            })
        return conversation

# Global enhanced chatbot instance
enhanced_clang = EnhancedClangChatbot()

async def get_clang_response(message: str, conversation_history: List = None) -> Dict[str, Any]:
    """
    Main entry point for getting enhanced Clang AI responses
    """
    return await enhanced_clang.get_enhanced_response(message, conversation_history)

# Compatibility function for existing code
async def get_enhanced_chatbot_response(message: str, history: List = None) -> str:
    """Simplified function that returns just the response text"""
    result = await get_clang_response(message, history)
    return result['response']
