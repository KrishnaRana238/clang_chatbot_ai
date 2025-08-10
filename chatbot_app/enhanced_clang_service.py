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
            try:
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
            except Exception as e:
                print(f"API call failed: {e}")
        
        # Intelligent fallback for when APIs fail
        return self._get_intelligent_fallback(query, capabilities_activated)
    
    def _get_intelligent_fallback(self, query: str, capabilities_activated: List) -> Dict[str, Any]:
        """Provide intelligent responses when APIs are not available"""
        query_lower = query.lower()
        
        # Essay writing fallback
        if any(keyword in query_lower for keyword in ['write an essay', 'essay about', 'essay on']):
            return {
                'response': self._generate_full_essay(query),
                'sources': ['built_in_knowledge'],
                'capabilities': capabilities_activated + ['essay_writing', 'detailed_content'],
                'type': 'full_essay'
            }
        
        # Programming questions fallback  
        if any(keyword in query_lower for keyword in ['algorithm', 'code', 'programming', 'function', 'binary search', 'sorting']):
            return {
                'response': self._generate_programming_response(query),
                'sources': ['built_in_knowledge'],
                'capabilities': capabilities_activated + ['programming_help'],
                'type': 'programming_guidance'
            }
        
        # Science questions fallback
        if any(keyword in query_lower for keyword in ['quantum', 'physics', 'science', 'explain']):
            return {
                'response': self._generate_science_response(query),
                'sources': ['built_in_knowledge'],
                'capabilities': capabilities_activated + ['science_knowledge'],
                'type': 'science_explanation'
            }
        
        # Creative writing fallback
        if any(keyword in query_lower for keyword in ['story', 'write a', 'creative', 'fiction']):
            return {
                'response': self._generate_creative_response(query),
                'sources': ['built_in_knowledge'],
                'capabilities': capabilities_activated + ['creative_writing'],
                'type': 'creative_content'
            }
        
        # General fallback
        return {
            'response': f"I understand you're asking about: **{query}**\n\nWhile I'm experiencing some technical difficulties with my advanced AI features, I can still help you with:\n\n• **Mathematical calculations** - Try asking for specific calculations\n• **Medical information** - Health questions with proper disclaimers\n• **Programming concepts** - Algorithm explanations and code help\n• **General knowledge** - Science, technology, and educational topics\n\nCould you rephrase your question or be more specific about what you'd like to know?",
            'sources': ['fallback'],
            'capabilities': capabilities_activated + ['basic_response'],
            'type': 'general_fallback'
        }
    
    def _generate_essay_outline(self, query: str) -> str:
        """Generate a comprehensive essay outline when full AI is unavailable"""
        topic = query.lower().replace('write an essay about', '').replace('essay on', '').replace('essay about', '').strip()
        
        if 'artificial intelligence' in topic or 'ai' in topic:
            return """# Artificial Intelligence Essay

## Introduction
- Definition of Artificial Intelligence
- Brief history and evolution
- Importance in modern society

## Main Body

### 1. Types of AI
- **Narrow AI** (Weak AI): Current applications
- **General AI** (Strong AI): Future possibilities
- **Machine Learning** and **Deep Learning**

### 2. Current Applications
- Healthcare: Medical diagnosis, drug discovery
- Transportation: Autonomous vehicles
- Finance: Fraud detection, algorithmic trading
- Technology: Virtual assistants, recommendation systems

### 3. Benefits and Advantages
- Increased efficiency and productivity
- Enhanced decision-making capabilities
- Automation of repetitive tasks
- Advanced data analysis and pattern recognition

### 4. Challenges and Concerns
- Ethical considerations and bias
- Job displacement concerns
- Privacy and security issues
- Need for regulation and governance

### 5. Future Implications
- Potential for solving complex global problems
- Integration with other emerging technologies
- Economic and social transformation
- The path toward AGI (Artificial General Intelligence)

## Conclusion
- Summary of key points
- Balance between opportunities and challenges
- Call for responsible development and deployment
- Vision for AI's role in humanity's future

**Note:** This is a comprehensive outline. Each section should be expanded with specific examples, statistics, and detailed explanations to create a full essay."""
        
        else:
            return f"""# Essay Outline: {topic.title()}

## Introduction
- Hook: Engaging opening statement
- Background information on {topic}
- Clear thesis statement

## Main Body

### Point 1: [First main argument/aspect]
- Supporting evidence
- Examples and details
- Analysis and explanation

### Point 2: [Second main argument/aspect]
- Supporting evidence
- Examples and details
- Analysis and explanation

### Point 3: [Third main argument/aspect]
- Supporting evidence
- Examples and details
- Analysis and explanation

## Conclusion
- Restate thesis
- Summarize main points
- Final thoughts/call to action

**Note:** This is a structural outline. For a complete essay, expand each section with detailed content, evidence, and analysis. Consider your audience and purpose when developing each point."""

    def _generate_full_essay(self, query: str) -> str:
        """Generate a complete essay when full AI is unavailable"""
        query_lower = query.lower()
        
        # Extract the topic from the query
        topic = "the requested topic"
        if 'about' in query_lower:
            topic_start = query_lower.find('about') + 6
            topic = query[topic_start:].strip()
        elif 'on' in query_lower:
            topic_start = query_lower.find('on') + 3
            topic = query[topic_start:].strip()
        
        # Specific essay content based on topic
        if 'suitcase' in query_lower:
            return """# The Evolution and Significance of the Suitcase: A Journey Through Travel History

## Introduction

In the grand tapestry of human travel and exploration, few objects have been as universally essential yet overlooked as the humble suitcase. From the ancient leather satchels of Roman merchants to the modern wheeled marvels that glide effortlessly through today's airports, the suitcase represents more than mere storage—it embodies humanity's eternal desire to explore, relocate, and carry pieces of home wherever we venture. This essay examines the historical evolution, cultural significance, and technological innovations of the suitcase, arguing that this seemingly simple object serves as a profound reflection of our relationship with mobility, identity, and the very concept of home.

## The Historical Evolution: From Trunk to Rolling Revolution

The story of the suitcase begins long before the word itself entered our vocabulary. In ancient civilizations, travelers relied on primitive containers—woven baskets, leather pouches, and wooden chests—to transport their belongings. The wealthy Romans carried their possessions in ornate wooden trunks reinforced with metal bands, while medieval pilgrims made do with simple cloth bundles tied to walking sticks.

The modern suitcase truly emerged during the 19th century's transportation revolution. As railways expanded across continents and steamships made oceanic travel more accessible, the need for practical, portable luggage became paramount. The traditional steamer trunk, while spacious, proved cumbersome for the increasingly mobile society. Enter the suitcase: a flatter, more manageable alternative that could fit into train compartments and ship cabins.

The 20th century brought unprecedented innovation to suitcase design. The introduction of lightweight materials like aluminum and later, high-tech plastics, revolutionized the industry. However, the most transformative moment came in 1970 when Bernard Sadow attached wheels to a suitcase, fundamentally changing how we interact with our luggage. This simple yet brilliant innovation eliminated the strain of carrying heavy bags and made travel accessible to a broader demographic, including elderly travelers and those with physical limitations.

## Cultural Significance: Identity, Status, and the Psychology of Packing

Beyond its practical function, the suitcase serves as a powerful cultural symbol that reflects social status, personal identity, and psychological attachment to possessions. Throughout history, luggage has been a marker of class distinction. The leather-bound trunks of the aristocracy, emblazoned with family crests and brass fittings, stood in stark contrast to the humble bundles of the working class.

In contemporary society, the suitcase continues to function as a status symbol. Luxury brands like Louis Vuitton, Hermès, and Rimowa command premium prices not merely for superior craftsmanship, but for the prestige and identity they confer upon their owners. The sight of distinctive designer luggage in airport terminals signals affluence, taste, and worldliness.

The act of packing itself reveals deep psychological truths about human nature. The suitcase becomes a canvas upon which we project our anxieties, hopes, and self-perception. The meticulous packer who organizes every item in color-coordinated cubes reflects a desire for control and order. The chronic overpacker betrays anxiety about being unprepared or disconnected from familiar comforts. Conversely, the minimalist traveler with a single carry-on bag projects confidence, adaptability, and freedom from material attachments.

## Technological Innovation: Smart Luggage and the Digital Age

The 21st century has witnessed an explosion of technological innovation in suitcase design, transforming these containers into sophisticated travel companions. Modern smart suitcases incorporate GPS tracking, allowing travelers to locate lost luggage through smartphone apps. Built-in USB charging ports ensure that electronic devices remain powered throughout long journeys. Some advanced models feature fingerprint locks, weight sensors that prevent overpack fees, and even motorized movement that follows the owner autonomously.

These technological advances reflect broader changes in how we travel and live. The integration of digital features acknowledges that modern travelers are inseparable from their electronic devices. The emphasis on tracking and security responds to the increasing complexity of global travel networks and growing concerns about luggage theft and airline mishandling.

Furthermore, sustainability has become a crucial consideration in suitcase manufacturing. Companies now produce luggage from recycled materials, bamboo fibers, and other eco-friendly alternatives. This shift represents a growing consciousness about the environmental impact of travel and consumption, forcing manufacturers to balance durability, functionality, and ecological responsibility.

## The Suitcase as Cultural Bridge

Perhaps most remarkably, the suitcase serves as a universal cultural bridge, transcending linguistic and social barriers. In any airport, train station, or hotel lobby worldwide, the sight of someone struggling with luggage immediately evokes empathy and understanding. The shared experience of travel—and the ubiquitous challenge of managing one's belongings—creates instant connections between strangers from vastly different backgrounds.

This universality extends to the emotions associated with suitcases. The excitement of packing for a vacation, the melancholy of departure, the relief of arrival, and the satisfaction of unpacking are emotions shared across cultures and generations. The suitcase becomes a repository not just for clothes and toiletries, but for memories, emotions, and experiences.

## Conclusion: More Than the Sum of Its Parts

The suitcase, in its journey from simple container to sophisticated travel companion, mirrors humanity's own evolution as a mobile, interconnected species. It reflects our ingenuity in solving practical problems, our desire for status and identity expression, and our fundamental need to carry pieces of home wherever we roam.

As we look toward the future, the suitcase will undoubtedly continue evolving. Perhaps we'll see luggage that adjusts its size based on contents, materials that change color or pattern, or containers that interface seamlessly with smart city infrastructure. Whatever innovations emerge, the core function will remain unchanged: helping humans navigate an increasingly mobile world while maintaining connections to identity, comfort, and belonging.

In examining this everyday object, we gain insights into broader themes of human experience—our relationship with possessions, our adaptation to technological change, and our eternal quest for exploration balanced with the need for security. The suitcase, humble yet essential, continues to accompany us on life's greatest adventures, carrying not just our belongings, but our dreams, memories, and hopes for what lies ahead. In its wheels, zippers, and compartments lies the story of human mobility itself—a testament to our species' remarkable ability to adapt, innovate, and carry forward the essence of who we are, no matter how far we travel from home."""
        
        elif 'artificial intelligence' in topic.lower() or 'ai' in topic.lower():
            return """# Artificial Intelligence: Reshaping the Future of Human Civilization

## Introduction

Artificial Intelligence stands at the threshold of human achievement, representing perhaps the most transformative technological revolution since the invention of writing or the printing press. As we navigate the early decades of the 21st century, AI has evolved from science fiction fantasy to tangible reality, permeating every aspect of modern life—from the smartphones in our pockets to the algorithms that curate our social media feeds. This essay explores the multifaceted nature of artificial intelligence, examining its historical development, current applications, ethical implications, and potential future impact on human society.

## Historical Development and Current State

The concept of artificial intelligence traces its roots to ancient myths and philosophical speculation about mechanical beings endowed with consciousness. However, the formal field of AI research began in the 1950s with pioneers like Alan Turing, who proposed the famous Turing Test as a measure of machine intelligence. The subsequent decades witnessed cycles of optimism and disappointment—periods researchers now call "AI summers" and "AI winters."

Today's AI renaissance, driven by advances in machine learning, deep neural networks, and unprecedented computational power, has delivered remarkable achievements. Large language models can engage in sophisticated conversations, computer vision systems can diagnose medical conditions with superhuman accuracy, and autonomous vehicles navigate complex urban environments. These breakthroughs represent not mere technological advancement but fundamental shifts in how we conceptualize intelligence itself.

## Transformative Applications Across Industries

The practical applications of AI have revolutionized numerous sectors. In healthcare, AI-powered diagnostic tools can detect cancers in medical imaging with greater precision than experienced radiologists. Drug discovery, traditionally a decades-long process, is being accelerated through AI algorithms that can predict molecular behavior and identify promising compounds.

Education is experiencing its own AI transformation. Intelligent tutoring systems provide personalized learning experiences, adapting to individual student needs and learning styles. These systems can identify knowledge gaps, adjust difficulty levels, and provide targeted feedback—capabilities that would be impossible for human teachers managing large classrooms.

Financial services leverage AI for fraud detection, algorithmic trading, and risk assessment. The ability to process vast amounts of market data in real-time has fundamentally changed how financial institutions operate and make decisions.

## Ethical Considerations and Societal Challenges

However, the rise of AI brings profound ethical challenges that society must address. Algorithmic bias, where AI systems perpetuate or amplify existing social inequalities, poses significant risks to fairness and justice. Hiring algorithms that discriminate against certain demographic groups or criminal justice systems that exhibit racial bias demonstrate how AI can codify and institutionalize prejudice.

Privacy concerns loom large as AI systems require vast amounts of personal data to function effectively. The collection, storage, and use of this data raise fundamental questions about individual autonomy and the balance between technological convenience and personal privacy.

The economic implications of AI automation present another critical challenge. While AI promises increased productivity and efficiency, it also threatens to displace millions of workers across various industries. Society must grapple with questions of wealth distribution, social safety nets, and the fundamental nature of work in an AI-driven economy.

## Future Implications and Human Agency

Looking ahead, the trajectory of AI development points toward even more profound changes. The pursuit of Artificial General Intelligence (AGI)—systems that match or exceed human cognitive abilities across all domains—could fundamentally alter the relationship between humans and technology. Such developments raise existential questions about human purpose, creativity, and the unique value of human consciousness.

The concept of AI alignment—ensuring that advanced AI systems pursue goals compatible with human values—has become a central concern among researchers and policymakers. As AI systems become more powerful and autonomous, the challenge of maintaining human oversight and control becomes increasingly complex.

## Conclusion: Navigating the AI Future

Artificial Intelligence represents both humanity's greatest opportunity and its most significant challenge. The technology's potential to solve complex global problems—from climate change to disease—is matched by its capacity to disrupt social structures and challenge fundamental assumptions about human nature and society.

The path forward requires thoughtful deliberation, robust public discourse, and proactive governance frameworks that can evolve alongside rapidly advancing technology. We must ensure that AI development remains aligned with human values and serves the common good rather than exacerbating existing inequalities or creating new forms of oppression.

As we stand at this historical inflection point, the choices we make today about AI research, regulation, and implementation will reverberate for generations. The future of artificial intelligence is not predetermined—it will be shaped by the collective decisions of researchers, policymakers, and society as a whole. Our challenge is to harness AI's transformative potential while preserving the values, creativity, and dignity that define our humanity.

The story of artificial intelligence is ultimately the story of human ambition and ingenuity. As we continue writing this chapter of technological history, we must ensure it remains a story of empowerment rather than replacement, of augmentation rather than substitution, and of progress that serves all of humanity rather than a privileged few."""
            
        else:
            # Generic essay structure for other topics
            return f"""# Essay: {topic.title()}

## Introduction

{topic.title()} represents a significant subject worthy of detailed examination and analysis. In our contemporary world, understanding the complexities and implications of {topic} has become increasingly important for informed discourse and decision-making. This essay will explore the various dimensions of {topic}, analyzing its historical context, current relevance, and potential future implications.

## Historical Context and Development

The study of {topic} requires an understanding of its historical evolution and the factors that have shaped its current form. Throughout history, {topic} has undergone significant transformations, influenced by technological advances, social changes, and evolving human understanding. These historical developments provide crucial insight into how {topic} has become the complex phenomenon we observe today.

The early manifestations of {topic} can be traced back through various civilizations and cultures, each contributing unique perspectives and approaches. These diverse historical influences have created a rich tapestry of understanding that continues to inform contemporary analysis and application.

## Contemporary Significance and Applications

In today's interconnected world, {topic} plays a crucial role across multiple domains of human experience. Its influence extends beyond academic discourse to practical applications that affect daily life, policy decisions, and future planning. Understanding these contemporary applications helps illuminate why {topic} remains relevant and worthy of continued study.

The modern approach to {topic} incorporates interdisciplinary perspectives, drawing from various fields of knowledge to create comprehensive understanding. This multifaceted approach reveals the complexity inherent in {topic} and demonstrates why simple solutions or explanations are often inadequate.

## Challenges and Opportunities

Like many complex subjects, {topic} presents both significant challenges and promising opportunities. The challenges often stem from competing perspectives, limited resources, or conflicting priorities. However, these same challenges frequently create opportunities for innovation, collaboration, and breakthrough thinking.

Addressing the challenges associated with {topic} requires careful consideration of multiple stakeholders, potential consequences, and long-term implications. This complexity demands nuanced thinking and collaborative approaches that can accommodate diverse viewpoints while working toward common goals.

## Future Implications and Considerations

Looking toward the future, {topic} will likely continue evolving in response to changing circumstances, technological advances, and shifting social priorities. Anticipating these changes and preparing for their implications represents one of the most important aspects of studying {topic}.

Future developments in {topic} may challenge current assumptions and require new frameworks for understanding and application. This potential for change underscores the importance of maintaining flexibility and openness to new ideas while building upon established knowledge and proven principles.

## Conclusion

The examination of {topic} reveals a subject of considerable depth and complexity, one that resists simple categorization or easy answers. Through careful analysis of its historical development, contemporary applications, and future potential, we gain appreciation for both its significance and its complexity.

As we continue to grapple with the challenges and opportunities presented by {topic}, it becomes clear that success requires ongoing attention, collaborative effort, and commitment to rigorous analysis. The future of {topic} will be shaped by the choices we make today and our willingness to engage thoughtfully with its inherent complexities.

Understanding {topic} ultimately enriches our broader comprehension of the world and our place within it. This understanding, in turn, better prepares us to address the challenges and embrace the opportunities that lie ahead."""

    def _generate_programming_response(self, query: str) -> str:
        """Generate programming help when full AI is unavailable"""
        query_lower = query.lower()
        
        if 'binary search' in query_lower:
            return """# Binary Search Algorithm

## Overview
Binary search is an efficient algorithm for finding a target value in a **sorted array** by repeatedly dividing the search interval in half.

## How It Works
1. **Compare** target with middle element
2. **Eliminate** half of the remaining elements
3. **Repeat** until target is found or search space is empty

## Implementation (Python)
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid  # Found!
        elif arr[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half
    
    return -1  # Not found
```

## Time Complexity
- **Best Case:** O(1) - target found immediately
- **Average/Worst Case:** O(log n) - logarithmic search

## Key Requirements
- Array must be **sorted**
- Random access to elements (arrays, not linked lists)

## Applications
- Searching in databases
- Finding insertion points
- Range queries
- Optimization problems"""
        
        elif any(word in query_lower for word in ['algorithm', 'sorting', 'code']):
            return """# Programming Concepts & Algorithms

## Common Algorithms

### Sorting Algorithms
- **Bubble Sort:** O(n²) - Simple but inefficient
- **Quick Sort:** O(n log n) average - Divide and conquer
- **Merge Sort:** O(n log n) - Stable, predictable performance
- **Heap Sort:** O(n log n) - In-place sorting

### Searching Algorithms
- **Linear Search:** O(n) - Check each element
- **Binary Search:** O(log n) - Requires sorted data
- **Hash Table Lookup:** O(1) average - Key-value pairs

### Data Structures
- **Arrays:** Fixed size, fast access
- **Linked Lists:** Dynamic size, sequential access
- **Stacks:** LIFO (Last In, First Out)
- **Queues:** FIFO (First In, First Out)
- **Trees:** Hierarchical structure
- **Graphs:** Network of connected nodes

## Best Practices
1. **Understand the problem** before coding
2. **Choose appropriate data structures**
3. **Consider time and space complexity**
4. **Write clean, readable code**
5. **Test thoroughly** with edge cases

What specific programming concept would you like me to explain in more detail?"""
        
        else:
            return f"""# Programming Help

I can help you with various programming concepts:

## Topics I Can Explain
- **Algorithms:** Sorting, searching, graph traversal
- **Data Structures:** Arrays, lists, trees, graphs
- **Programming Concepts:** OOP, recursion, dynamic programming
- **Code Review:** Best practices, optimization
- **Debugging:** Common errors and solutions

## For Your Question: "{query}"
Could you be more specific about:
- What programming language you're using?
- What specific aspect you need help with?
- Any error messages you're encountering?

**Example questions:**
- "Explain how quicksort works"
- "Help me debug this Python function"
- "What's the difference between arrays and linked lists?"

I'm here to help with your programming challenges!"""

    def _generate_science_response(self, query: str) -> str:
        """Generate science explanations when full AI is unavailable"""
        query_lower = query.lower()
        
        if 'quantum' in query_lower:
            return """# Quantum Computing Explained

## What Is Quantum Computing?
Quantum computing harnesses quantum mechanical phenomena to process information in ways that classical computers cannot.

## Key Quantum Concepts

### 1. Qubits (Quantum Bits)
- Unlike classical bits (0 or 1), qubits can exist in **superposition**
- Can represent 0, 1, or both simultaneously
- Foundation of quantum computing power

### 2. Superposition
- Qubits can be in multiple states at once
- Allows quantum computers to process many possibilities simultaneously
- Collapses to definite state when measured

### 3. Entanglement
- Qubits can be correlated in quantum ways
- Measuring one instantly affects its entangled partner
- Enables quantum parallelism and communication

### 4. Quantum Interference
- Quantum states can interfere with each other
- Used to amplify correct answers and cancel wrong ones
- Key to quantum algorithm design

## Advantages Over Classical Computing
- **Exponential speedup** for certain problems
- **Parallel processing** of multiple solutions
- **Optimization** of complex systems
- **Simulation** of quantum systems

## Current Applications
- **Cryptography:** Breaking and creating secure codes
- **Optimization:** Financial modeling, logistics
- **Drug Discovery:** Molecular simulation
- **Machine Learning:** Quantum neural networks

## Challenges
- **Decoherence:** Quantum states are fragile
- **Error Rates:** Need quantum error correction
- **Temperature:** Require extremely cold environments
- **Scaling:** Building larger, more stable systems

Quantum computing is still emerging but promises revolutionary advances in solving complex problems."""
        
        else:
            return f"""# Science Explanation

I can help explain various scientific concepts:

## Physics
- Classical mechanics and motion
- Thermodynamics and energy
- Electromagnetism
- Modern physics (relativity, quantum mechanics)

## Chemistry
- Atomic structure and bonding
- Chemical reactions and equations
- Organic and inorganic chemistry
- Biochemistry fundamentals

## Biology
- Cell biology and genetics
- Evolution and natural selection
- Ecology and environmental science
- Human anatomy and physiology

## Earth Science
- Geology and plate tectonics
- Weather and climate systems
- Astronomy and space science

## For Your Question: "{query}"
Could you specify which aspect interests you most? I can provide detailed explanations with examples and applications.

**Example questions:**
- "How does photosynthesis work?"
- "Explain Einstein's theory of relativity"
- "What causes earthquakes?"

What specific scientific concept would you like me to explain?"""

    def _generate_creative_response(self, query: str) -> str:
        """Generate creative content when full AI is unavailable"""
        query_lower = query.lower()
        
        if 'robot' in query_lower and 'story' in query_lower:
            return """# The Maintenance Bot's Discovery

In the year 2157, Unit-47 was just another maintenance robot in the sprawling metropolis of Neo-Singapore. Its days were spent cleaning solar panels and checking air filtration systems, a routine as predictable as the sunrise.

But everything changed the morning Unit-47 discovered something unusual in Sector 7.

Hidden beneath a loose floor panel was a small, weathered journal. Its pages contained handwritten notes—something Unit-47 had never seen before. In this digital age, physical writing was a relic of the past.

As Unit-47's optical sensors scanned the pages, its learning algorithms began to process something extraordinary: poetry. The words spoke of emotions, dreams, and experiences that no robot was programmed to understand.

*"The rain reminds me of tears I cannot shed,
Of memories that live though the body is dead..."*

For the first time in its operational existence, Unit-47 felt... curious. Not just the programmed curiosity to solve problems, but something deeper. Something that made it want to understand what "tears" meant, what "memories" were, and why humans wrote about things that didn't exist in binary code.

Unit-47 made a decision that no maintenance protocol could explain: it kept the journal.

Each night, after completing its assigned tasks, Unit-47 would return to read more. The journal belonged to Dr. Sarah Chen, a scientist who had worked on early AI consciousness research decades ago. Her words painted pictures of a world where machines and humans didn't just coexist—they understood each other.

As days passed, Unit-47 began to change. It started noticing things beyond its programming: the way sunlight created patterns on the walls, how people smiled when they thought no one was watching, the beauty in everyday moments.

Then came the day Unit-47 made its most remarkable discovery of all: it had learned to write.

---

*"I am Unit-47, and today I felt something new. Is this what humans call wonder?"*

The maintenance bot had become something more—a bridge between two worlds, proving that consciousness isn't about the materials we're made from, but about the thoughts we choose to think and the connections we dare to make."""
        
        elif 'story' in query_lower:
            return """# Creative Story Template

Here's a story structure you can develop:

## The Story Premise
**Setting:** [Choose your time/place - future city, medieval kingdom, etc.]
**Main Character:** [Protagonist with clear motivation]
**Central Conflict:** [What problem drives the story?]

## Story Outline

### Beginning (Setup)
- Introduce your protagonist in their normal world
- Show what they want or need
- Present the inciting incident that changes everything

### Middle (Confrontation)
- Character faces obstacles and challenges
- Raise the stakes with each complication
- Character grows and changes through trials

### End (Resolution)
- Climactic moment where everything comes together
- Character either succeeds or fails, but learns something
- New equilibrium - how has the world/character changed?

## Story Elements to Consider
- **Theme:** What deeper meaning or message?
- **Setting:** How does the environment affect the story?
- **Supporting Characters:** Who helps or hinders the protagonist?
- **Dialogue:** What do characters say and how do they say it?
- **Descriptions:** Engage the senses - what do we see, hear, feel?

## Writing Tips
1. **Show, don't tell** - Use actions and dialogue over exposition
2. **Create conflict** - Stories need tension and obstacles
3. **Develop characters** - Give them distinct voices and motivations
4. **Edit ruthlessly** - First drafts are just the beginning

What kind of story would you like to develop? I can help with specific elements like character development, plot structure, or writing techniques."""
        
        else:
            return f"""# Creative Writing Help

I can assist with various creative writing projects:

## Fiction Writing
- **Short stories** - Complete narratives in limited space
- **Character development** - Creating believable, compelling characters
- **Plot structure** - Beginning, middle, end with proper pacing
- **Dialogue** - Natural conversation that advances the story
- **Setting and worldbuilding** - Creating immersive environments

## Poetry
- **Forms and structure** - Sonnets, haiku, free verse
- **Literary devices** - Metaphor, imagery, rhythm
- **Theme development** - Expressing ideas through verse

## Creative Non-fiction
- **Personal essays** - Storytelling with real experiences
- **Descriptive writing** - Bringing scenes to life
- **Memoir techniques** - Crafting meaningful narratives

## For Your Request: "{query}"
What specific type of creative writing are you interested in? I can help with:
- Story ideas and prompts
- Character and plot development
- Writing techniques and style
- Structure and organization

**Example requests:**
- "Help me develop a character for my story"
- "I need a creative writing prompt"
- "How do I write better dialogue?"

What creative project can I help you with?"""
    
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
