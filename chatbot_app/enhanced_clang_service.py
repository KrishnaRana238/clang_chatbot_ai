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
    from .medical_knowledge_service import medical_service, get_medical_information
    from .chatbot_service import OpenSourceChatbotService
    from .conversation_memory import ConversationMemory
    from .human_interaction import interaction_optimizer
    HAS_ENHANCED_SERVICES = True
    HAS_MEDICAL_SERVICE = True
    HAS_MEMORY_SERVICE = True
    HAS_HUMAN_INTERACTION = True
except ImportError as e:
    print(f"⚠️  Enhanced services not available: {e}")
    HAS_ENHANCED_SERVICES = False
    HAS_MEDICAL_SERVICE = False
    HAS_MEMORY_SERVICE = False
    HAS_HUMAN_INTERACTION = False
    try:
        from .chatbot_service import OpenSourceChatbotService
        try:
            from .medical_knowledge_service import medical_service, get_medical_information
            HAS_MEDICAL_SERVICE = True
        except ImportError:
            print("⚠️  Medical service not available")
            HAS_MEDICAL_SERVICE = False
        try:
            from .conversation_memory import ConversationMemory
            HAS_MEMORY_SERVICE = True
        except ImportError:
            print("⚠️  Memory service not available")
            HAS_MEMORY_SERVICE = False
        try:
            from .human_interaction import interaction_optimizer
            HAS_HUMAN_INTERACTION = True
        except ImportError:
            print("⚠️  Human interaction service not available")
            HAS_HUMAN_INTERACTION = False
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
    - Medical knowledge and healthcare assistance
    - Conversational AI with context awareness
    """
    
    def __init__(self):
        self.name = "Clang"
        self.version = "2.0 Advanced Medical"
        self.capabilities = {
            'knowledge_base': True,
            'nlp_processing': True,
            'grammar_checking': True,
            'math_solving': True,
            'code_generation': True,
            'paraphrasing': True,
            'medical_assistance': HAS_MEDICAL_SERVICE,
            'drug_information': HAS_MEDICAL_SERVICE,
            'symptom_analysis': HAS_MEDICAL_SERVICE,
            'first_aid_guidance': HAS_MEDICAL_SERVICE,
            'conversation_memory': HAS_MEMORY_SERVICE,
            'human_interaction': HAS_HUMAN_INTERACTION,
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
        
        # Initialize conversation memory system
        if HAS_MEMORY_SERVICE:
            try:
                self.memory = ConversationMemory()
                print("✅ Conversation memory system initialized")
            except Exception as e:
                print(f"⚠️ Memory system failed to initialize: {e}")
                self.memory = None
        else:
            self.memory = None
        
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
    
    async def get_enhanced_response(self, user_message: str, conversation_history: List = None, user_id: str = None) -> Dict[str, Any]:
        """
        Main method to process user queries with full AI capabilities
        Returns comprehensive response with metadata
        """
        
        start_time = datetime.now()
        self.session_stats['queries_processed'] += 1
        
        try:
            # Step 1: Get user context from memory system
            user_context = {}
            if self.memory and user_id:
                user_context = self.memory.get_user_context(user_id)
            
            # Step 2: Advanced NLP Analysis
            if HAS_ENHANCED_SERVICES:
                nlp_analysis = await process_user_query(user_message)
                analysis = nlp_analysis['analysis']
                response_strategy = nlp_analysis['response_strategy']
            else:
                # Fallback to basic analysis
                analysis = None
                response_strategy = {'should_search_knowledge': True, 'complexity_level': 'medium'}
            
            # Step 3: Route to appropriate handler based on intent
            response_data = await self._route_query(user_message, analysis, response_strategy, conversation_history)
            
            # Step 4: Enhance response with context and personality
            final_response = self._enhance_response_with_personality(response_data, analysis)
            
            # Step 5: Apply human interaction optimization
            if HAS_HUMAN_INTERACTION:
                final_response = interaction_optimizer.make_response_conversational(
                    final_response, user_message, user_context
                )
            
            # Step 6: Update conversation memory
            self._update_conversation_memory(user_message, final_response, analysis)
            
            # Step 7: Save to persistent memory if available
            if self.memory and user_id:
                self.memory.save_conversation(
                    user_id=user_id,
                    user_message=user_message,
                    bot_response=final_response,
                    intent=analysis.intent if analysis else 'unknown',
                    metadata={'sources': response_data.get('sources', [])},
                    context=user_context
                )
            
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
                    'session_stats': self.session_stats.copy(),
                    'user_context': user_context if user_context else {}
                },
                'conversation_context': {
                    'memory_items': len(self.conversation_memory),
                    'user_preferences': self.user_preferences,
                    'suggested_followup': self._generate_followup_suggestions(analysis, response_data),
                    'interaction_count': user_context.get('profile', {}).get('interaction_count', 0) if user_context else 0
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
        
        # Handle medical queries
        if strategy.get('should_provide_medical_info', False) or self._is_medical_query(query):
            capabilities_activated.append('medical_assistant')
            
            if HAS_MEDICAL_SERVICE:
                medical_info = self._handle_medical_query(query)
                sources_used.append('medical_knowledge_base')
                
                return {
                    'response': medical_info['response'],
                    'sources': sources_used,
                    'capabilities': capabilities_activated,
                    'type': 'medical_information',
                    'medical_data': medical_info.get('data', {})
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
            
            # Check if response is valid
            if llm_response and llm_response.strip():
                return {
                    'response': llm_response,
                    'sources': sources_used,
                    'capabilities': capabilities_activated,
                    'type': 'general_conversation'
                }
            else:
                return {
                    'response': "I'm having trouble generating a response right now. Could you please try rephrasing your question?",
                    'sources': ['fallback'],
                    'capabilities': ['basic_response'],
                    'type': 'fallback'
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
        if base_response is None:
            base_response = "I encountered an issue while processing your request. Let me try a different approach."
        
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

    def _is_medical_query(self, query: str) -> bool:
        """Check if the query is medical-related"""
        medical_keywords = [
            'symptom', 'disease', 'medication', 'drug', 'treatment', 'cure', 'medicine',
            'pain', 'fever', 'headache', 'nausea', 'vomiting', 'cough', 'cold', 'flu',
            'diabetes', 'hypertension', 'dengue', 'malaria', 'covid', 'infection',
            'antibiotic', 'paracetamol', 'aspirin', 'prescription', 'side effect',
            'dosage', 'first aid', 'emergency', 'doctor', 'hospital', 'medical',
            'health', 'illness', 'sick', 'hurt', 'injury', 'wound', 'bleeding',
            # Add all medications from our database
            'ibuprofen', 'atorvastatin', 'metformin', 'lisinopril', 'sumatriptan',
            'amoxicillin', 'omeprazole', 'cetirizine', 'acetaminophen', 'tylenol',
            'advil', 'motrin', 'lipitor', 'prilosec', 'zyrtec',
            # Add first aid/emergency terms
            'heart attack', 'choking', 'cpr', 'resuscitation'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in medical_keywords)
    
    def _extract_medical_keywords(self, query: str) -> str:
        """Extract medical keywords from natural language queries"""
        # All medications from our database (including brand names)
        medication_terms = [
            'paracetamol', 'acetaminophen', 'tylenol', 'panadol', 'calpol',
            'aspirin', 'acetylsalicylic', 'bayer', 'bufferin', 'ecotrin',
            'ibuprofen', 'advil', 'motrin', 'nurofen',
            'atorvastatin', 'lipitor',
            'metformin', 'glucophage', 'glumetza', 'fortamet',
            'lisinopril',
            'sumatriptan', 'imitrex',
            'amoxicillin', 'amoxil', 'trimox', 'moxatag',
            'omeprazole', 'prilosec', 'losec',
            'cetirizine', 'zyrtec', 'reactine'
        ]
        
        # Medical conditions from our database
        condition_terms = [
            'dengue', 'malaria', 'diabetes', 'hypertension', 'migraine', 'asthma',
            'fever', 'headache', 'pain', 'cold', 'flu', 'cough', 'infection'
        ]
        
        # First aid terms
        first_aid_terms = [
            'heart attack', 'stroke', 'bleeding', 'choking', 'burn', 'fracture',
            'emergency', 'first aid'
        ]
        
        # Combine all medical terms
        all_medical_terms = medication_terms + condition_terms + first_aid_terms
        
        # Remove common words that might interfere with search
        stop_words = ['tell', 'me', 'about', 'what', 'is', 'are', 'the', 'for', 'how', 'when', 'where', 'why', 'information', 'details', 'does', 'work', 'side', 'effects']
        
        # Find medical terms in the query (prioritize exact medication matches)
        query_lower = query.lower()
        
        # First, look for exact medication matches
        for term in medication_terms:
            if term in query_lower:
                return term
        
        # Then look for condition matches
        for term in condition_terms:
            if term in query_lower:
                return term
                
        # Then look for first aid matches
        for term in first_aid_terms:
            if term in query_lower:
                return term
        
        # If no specific medical terms found, clean the query
        words = query_lower.split()
        cleaned_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return ' '.join(cleaned_words) if cleaned_words else query

    def _handle_medical_query(self, query: str) -> Dict[str, Any]:
        """Handle medical information queries"""
        query_lower = query.lower()
        
        # Extract medical keywords from natural language
        medical_keywords = self._extract_medical_keywords(query_lower)
        search_query = medical_keywords if medical_keywords else query
        
        # Determine query type
        if any(word in query_lower for word in ['medication', 'drug', 'medicine', 'antibiotic', 'paracetamol', 'aspirin', 'ibuprofen', 'atorvastatin', 'metformin', 'lisinopril', 'sumatriptan', 'amoxicillin', 'omeprazole', 'cetirizine', 'acetaminophen', 'tylenol', 'advil', 'motrin', 'lipitor', 'prilosec', 'zyrtec', 'side effect', 'dosage']):
            query_type = 'medication'
        elif any(word in query_lower for word in ['first aid', 'emergency', 'bleeding', 'choking', 'heart attack']):
            query_type = 'first_aid'
        elif any(word in query_lower for word in ['symptom', 'feel', 'pain', 'hurt', 'sick']):
            query_type = 'symptoms'
        elif 'interaction' in query_lower:
            query_type = 'interactions'
        else:
            query_type = 'condition'
        
        # Get medical information using extracted keywords
        medical_result = get_medical_information(search_query, query_type)
        
        # Format response
        response = self._format_medical_response(medical_result, query_type)
        
        return {
            'response': response,
            'data': medical_result,
            'type': query_type
        }
    
    def _format_medical_response(self, medical_data: Dict, query_type: str) -> str:
        """Format medical information into readable response"""
        
        response = "🏥 **Medical Information**\n\n"
        
        if query_type == 'condition' and medical_data.get('conditions'):
            for condition in medical_data['conditions']:
                response += f"## {condition['condition_name']} ({condition['category']})\n\n"
                response += f"**🔍 Symptoms:** {condition['symptoms']}\n\n"
                response += f"**🎯 Causes:** {condition['causes']}\n\n"
                response += f"**💊 Treatments:** {condition['treatments']}\n\n"
                response += f"**💉 Medications:** {condition['medications']}\n\n"
                response += f"**⚠️ Severity:** {condition['severity_level']}\n\n"
                response += f"**🛡️ Prevention:** {condition['prevention']}\n\n"
                response += f"**🚨 See Doctor When:** {condition['when_to_see_doctor']}\n\n"
                if condition['complications']:
                    response += f"**⚡ Possible Complications:** {condition['complications']}\n\n"
                response += "---\n\n"
        
        elif query_type == 'medication' and medical_data.get('medications'):
            for med in medical_data['medications']:
                response += f"## {med['drug_name']} ({med['generic_name']})\n\n"
                response += f"**🏷️ Brand Names:** {med['brand_names']}\n\n"
                response += f"**🧬 Drug Class:** {med['drug_class']}\n\n"
                response += f"**🎯 Used For:** {med['indication']}\n\n"
                response += f"**💊 Available Forms:** {med['dosage_forms']}\n\n"
                response += f"**📏 Common Dosages:** {med['common_dosages']}\n\n"
                response += f"**⚠️ Side Effects:** {med['side_effects']}\n\n"
                response += f"**🚫 Contraindications:** {med['contraindications']}\n\n"
                response += f"**🔄 Drug Interactions:** {med['interactions']}\n\n"
                response += f"**🤰 Pregnancy Category:** {med['pregnancy_category']}\n\n"
                response += f"**🧪 How It Works:** {med['mechanism_of_action']}\n\n"
                response += "---\n\n"
        
        elif query_type == 'first_aid' and medical_data.get('first_aid'):
            for aid in medical_data['first_aid']:
                response += f"## 🚨 {aid['emergency_type']} - First Aid\n\n"
                response += f"**⚡ Immediate Steps:**\n{aid['immediate_steps']}\n\n"
                response += f"**🚫 Things to Avoid:**\n{aid['things_to_avoid']}\n\n"
                response += f"**📞 Call 911 When:**\n{aid['when_to_call_911']}\n\n"
                response += f"**🧰 Materials Needed:**\n{aid['materials_needed']}\n\n"
                response += "---\n\n"
        
        elif query_type == 'symptoms' and medical_data.get('possible_conditions'):
            response += "**🔍 Based on your symptoms, here are possible conditions:**\n\n"
            for condition in medical_data['possible_conditions']:
                response += f"• **{condition['condition_name']}** ({condition['category']})\n"
                response += f"  - Severity: {condition['severity_level']}\n"
                response += f"  - See doctor when: {condition['when_to_see_doctor']}\n\n"
        
        elif query_type == 'interactions' and medical_data.get('interactions_found'):
            response += "**🔄 Drug Interaction Information:**\n\n"
            for interaction in medical_data['interactions_found']:
                response += f"• **{interaction['medication']}**\n"
                response += f"  - Interactions: {interaction['interactions']}\n"
                response += f"  - Contraindications: {interaction['contraindications']}\n\n"
        
        # Add general search results if available - removed this problematic section
        # The medical data structure varies by query type, so this logic was causing issues
        
        # Add medical disclaimer
        response += "\n" + "⚠️" * 50 + "\n"
        response += "**🩺 MEDICAL DISCLAIMER**\n\n"
        response += "This information is for educational purposes only and should not replace professional medical advice. "
        response += "Always consult with a qualified healthcare provider for proper diagnosis, treatment, and medical care. "
        response += "In case of emergency, call your local emergency number immediately.\n"
        response += "⚠️" * 50 + "\n"
        
        return response

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

    def optimize_for_user(self, user_id: str, feedback: Dict[str, Any]):
        """Optimize chatbot behavior based on user feedback"""
        if not self.memory:
            return
        
        try:
            # Update user preferences based on feedback
            preferences = {
                'response_length': feedback.get('preferred_length', 'medium'),
                'communication_style': feedback.get('style', 'friendly'),
                'topics_of_interest': feedback.get('interests', []),
                'expertise_level': feedback.get('expertise', 'beginner')
            }
            
            self.memory.update_user_preferences(user_id, preferences)
            
            # Update human interaction personality based on feedback
            if HAS_HUMAN_INTERACTION and feedback.get('personality_feedback'):
                personality_updates = feedback['personality_feedback']
                
                if 'friendliness' in personality_updates:
                    interaction_optimizer.personality['friendliness'] = max(0, min(1, personality_updates['friendliness']))
                if 'formality' in personality_updates:
                    interaction_optimizer.personality['formality'] = max(0, min(1, personality_updates['formality']))
                if 'enthusiasm' in personality_updates:
                    interaction_optimizer.personality['enthusiasm'] = max(0, min(1, personality_updates['enthusiasm']))
                if 'empathy' in personality_updates:
                    interaction_optimizer.personality['empathy'] = max(0, min(1, personality_updates['empathy']))
                if 'humor' in personality_updates:
                    interaction_optimizer.personality['humor'] = max(0, min(1, personality_updates['humor']))
            
            print(f"✅ User {user_id} preferences updated successfully")
            
        except Exception as e:
            print(f"⚠️ Failed to optimize for user {user_id}: {e}")

    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user interaction patterns"""
        if not self.memory:
            return {}
        
        try:
            patterns = self.memory.analyze_conversation_patterns(user_id)
            return {
                'interaction_count': patterns.get('interaction_count', 0),
                'common_topics': patterns.get('common_topics', []),
                'preferred_response_types': patterns.get('preferred_response_types', []),
                'avg_session_length': patterns.get('avg_session_length', 0),
                'satisfaction_score': patterns.get('satisfaction_score', 0.5),
                'learning_progress': patterns.get('learning_progress', {}),
                'engagement_level': patterns.get('engagement_level', 'medium')
            }
        except Exception as e:
            print(f"⚠️ Failed to get insights for user {user_id}: {e}")
            return {}

    def train_from_conversation(self, user_id: str, conversation_data: List[Dict]):
        """Train the chatbot from conversation data for more human-like responses"""
        if not self.memory:
            print("⚠️ Memory system not available for training")
            return
        
        try:
            # Analyze conversation patterns
            for interaction in conversation_data:
                user_message = interaction.get('user_message', '')
                bot_response = interaction.get('bot_response', '')
                user_feedback = interaction.get('feedback', {})
                
                # Extract learning insights
                if user_feedback.get('rating', 0) >= 4:  # Good responses
                    # Learn from successful interactions
                    if 'response_style' in user_feedback:
                        self.memory.update_user_preferences(
                            user_id, 
                            {'preferred_style': user_feedback['response_style']}
                        )
                
                # Identify conversation patterns
                if HAS_HUMAN_INTERACTION:
                    emotion_analysis = interaction_optimizer.analyze_user_emotion(user_message)
                    
                    # Save emotional context for future responses
                    self.memory.save_conversation(
                        user_id=user_id,
                        user_message=user_message,
                        bot_response=bot_response,
                        intent=emotion_analysis.get('primary_emotion', 'neutral'),
                        metadata={
                            'emotions': emotion_analysis.get('emotions', []),
                            'sentiment': emotion_analysis.get('sentiment', 'neutral'),
                            'user_feedback': user_feedback
                        }
                    )
            
            print(f"✅ Training completed for user {user_id} with {len(conversation_data)} interactions")
            
        except Exception as e:
            print(f"⚠️ Training failed for user {user_id}: {e}")

# Global enhanced chatbot instance
enhanced_clang = EnhancedClangChatbot()

async def get_clang_response(message: str, conversation_history: List = None, user_id: str = None) -> Dict[str, Any]:
    """
    Main entry point for getting enhanced Clang AI responses with user context
    """
    return await enhanced_clang.get_enhanced_response(message, conversation_history, user_id)

# Compatibility function for existing code
async def get_enhanced_chatbot_response(message: str, history: List = None) -> str:
    """Simplified function that returns just the response text"""
    result = await get_clang_response(message, history)
    return result['response']
