"""
Advanced Knowledge Base Service for Clang AI
Comprehensive knowledge integration across multiple domains
"""

import os
import json
import re
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import requests
from dataclasses import dataclass
import asyncio
import aiohttp

# Try to import advanced NLP libraries
try:
    import spacy
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False
    print("📚 SpaCy not installed. Install with: pip install spacy")

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False
    print("📚 TextBlob not installed. Install with: pip install textblob")

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False
    print("📚 NLTK not installed. Install with: pip install nltk")

try:
    import sympy as sp
    from sympy import symbols, solve, simplify, expand, factor, diff, integrate
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False
    print("🔢 SymPy not installed. Install with: pip install sympy")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("🔢 NumPy not installed. Install with: pip install numpy")

@dataclass
class KnowledgeItem:
    """Represents a single knowledge base item"""
    id: str
    topic: str
    category: str
    content: str
    keywords: List[str]
    difficulty_level: str  # beginner, intermediate, advanced
    last_updated: datetime
    source: str
    confidence_score: float

@dataclass
class QueryResult:
    """Represents search results from knowledge base"""
    items: List[KnowledgeItem]
    total_score: float
    query_intent: str
    suggested_actions: List[str]

class KnowledgeBaseService:
    """Comprehensive Knowledge Base Management System"""
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = db_path
        self.categories = {
            'coding': {
                'subcategories': ['python', 'javascript', 'cpp', 'java', 'web_dev', 'algorithms', 'data_structures'],
                'keywords': ['programming', 'coding', 'syntax', 'function', 'class', 'variable', 'loop', 'api']
            },
            'history': {
                'subcategories': ['world_history', 'ancient', 'modern', 'wars', 'civilizations', 'cultural'],
                'keywords': ['history', 'historical', 'ancient', 'civilization', 'war', 'culture', 'timeline']
            },
            'geography': {
                'subcategories': ['countries', 'cities', 'landmarks', 'cultures', 'climate', 'demographics'],
                'keywords': ['geography', 'country', 'city', 'location', 'landmark', 'culture', 'population']
            },
            'politics': {
                'subcategories': ['government', 'policies', 'current_events', 'democracy', 'elections', 'international'],
                'keywords': ['politics', 'government', 'policy', 'election', 'democracy', 'law', 'constitution']
            },
            'writing': {
                'subcategories': ['grammar', 'style', 'composition', 'rhetoric', 'creative', 'academic'],
                'keywords': ['writing', 'grammar', 'style', 'essay', 'composition', 'rhetoric', 'language']
            },
            'mathematics': {
                'subcategories': ['algebra', 'calculus', 'geometry', 'statistics', 'discrete', 'applied'],
                'keywords': ['math', 'mathematics', 'equation', 'formula', 'calculate', 'solve', 'proof']
            },
            'science': {
                'subcategories': ['physics', 'chemistry', 'biology', 'computer_science', 'engineering'],
                'keywords': ['science', 'physics', 'chemistry', 'biology', 'experiment', 'theory', 'research']
            }
        }
        
        # Initialize NLP components
        self.nlp_processor = None
        self.lemmatizer = None
        self.stop_words = set()
        
        self._init_database()
        self._init_nlp_components()
        self._load_default_knowledge()
    
    def _init_database(self):
        """Initialize SQLite database for knowledge storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_items (
                id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                keywords TEXT NOT NULL,
                difficulty_level TEXT NOT NULL,
                last_updated DATETIME NOT NULL,
                source TEXT NOT NULL,
                confidence_score REAL NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                intent TEXT,
                results_count INTEGER,
                timestamp DATETIME NOT NULL,
                user_satisfaction REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Knowledge base database initialized")
    
    def _init_nlp_components(self):
        """Initialize NLP processing components"""
        if HAS_SPACY:
            try:
                self.nlp_processor = spacy.load("en_core_web_sm")
                print("✅ SpaCy NLP processor loaded")
            except OSError:
                print("⚠️  SpaCy model not found. Run: python -m spacy download en_core_web_sm")
        
        if HAS_NLTK:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('wordnet', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                
                self.lemmatizer = WordNetLemmatizer()
                self.stop_words = set(stopwords.words('english'))
                print("✅ NLTK components initialized")
            except:
                print("⚠️  NLTK initialization failed")
    
    def _load_default_knowledge(self):
        """Load comprehensive default knowledge base"""
        default_knowledge = [
            # Programming Knowledge
            {
                'id': 'coding_001',
                'topic': 'Python Basics',
                'category': 'coding',
                'content': '''Python is a high-level, interpreted programming language known for its simplicity and readability. 
                Key features: Dynamic typing, object-oriented, extensive standard library, cross-platform compatibility.
                Basic syntax: Variables (x = 10), Functions (def function_name():), Classes (class MyClass:), 
                Control structures (if/elif/else, for/while loops), Data structures (lists, dictionaries, tuples, sets).
                Popular frameworks: Django (web), Flask (web), NumPy (scientific), Pandas (data analysis), TensorFlow (ML).''',
                'keywords': ['python', 'programming', 'syntax', 'variables', 'functions', 'classes', 'loops'],
                'difficulty_level': 'beginner',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.95
            },
            {
                'id': 'coding_002',
                'topic': 'JavaScript Fundamentals',
                'category': 'coding',
                'content': '''JavaScript is a versatile programming language primarily used for web development.
                Core concepts: Variables (let, const, var), Functions (function, arrow functions), Objects, Arrays, 
                DOM manipulation, Event handling, Asynchronous programming (Promises, async/await).
                Modern features: ES6+ syntax, modules, destructuring, template literals, spread operator.
                Frameworks: React (UI), Vue.js (progressive), Angular (full framework), Node.js (server-side).''',
                'keywords': ['javascript', 'web', 'dom', 'functions', 'async', 'promises', 'react'],
                'difficulty_level': 'beginner',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.95
            },
            {
                'id': 'coding_003',
                'topic': 'Data Structures and Algorithms',
                'category': 'coding',
                'content': '''Data Structures: Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, Hash Tables.
                Algorithms: Sorting (Quick, Merge, Bubble), Searching (Binary, Linear), Graph traversal (DFS, BFS),
                Dynamic Programming, Greedy Algorithms, Divide and Conquer.
                Time Complexity: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n²) quadratic.
                Space Complexity: Amount of memory used by algorithm relative to input size.''',
                'keywords': ['algorithms', 'data structures', 'sorting', 'searching', 'complexity', 'big o'],
                'difficulty_level': 'intermediate',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.90
            },
            
            # History Knowledge
            {
                'id': 'history_001',
                'topic': 'World War II Overview',
                'category': 'history',
                'content': '''World War II (1939-1945) was the deadliest conflict in human history.
                Key events: Germany invades Poland (1939), Pearl Harbor attack (1941), D-Day landings (1944), 
                Atomic bombs on Japan (1945). Major powers: Allies (US, UK, USSR, China) vs Axis (Germany, Japan, Italy).
                Consequences: ~70-85 million deaths, formation of UN, beginning of Cold War, decolonization movement.
                Holocaust: Systematic genocide of 6 million Jews and millions of others by Nazi Germany.''',
                'keywords': ['world war', 'hitler', 'holocaust', 'allies', 'axis', 'pearl harbor', 'nazi'],
                'difficulty_level': 'intermediate',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.92
            },
            {
                'id': 'history_002',
                'topic': 'Ancient Civilizations',
                'category': 'history',
                'content': '''Major ancient civilizations shaped human development:
                Mesopotamia (3500-539 BCE): Cradle of civilization, writing system (cuneiform), Code of Hammurabi.
                Ancient Egypt (3100-30 BCE): Pyramids, hieroglyphs, pharaohs, Nile River civilization.
                Ancient Greece (800-146 BCE): Democracy, philosophy (Socrates, Plato, Aristotle), Olympic Games.
                Roman Empire (27 BCE-476/1453 CE): Law system, engineering, military tactics, spread of Christianity.
                Ancient China: Great Wall, Silk Road, inventions (paper, gunpowder, compass), dynasties.''',
                'keywords': ['ancient', 'civilization', 'egypt', 'greece', 'rome', 'mesopotamia', 'china'],
                'difficulty_level': 'intermediate',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.88
            },
            
            # Geography Knowledge
            {
                'id': 'geography_001',
                'topic': 'World Countries and Capitals',
                'category': 'geography',
                'content': '''Major countries and capitals by continent:
                North America: USA (Washington DC), Canada (Ottawa), Mexico (Mexico City)
                South America: Brazil (Brasília), Argentina (Buenos Aires), Colombia (Bogotá)
                Europe: UK (London), France (Paris), Germany (Berlin), Italy (Rome), Spain (Madrid)
                Asia: China (Beijing), Japan (Tokyo), India (New Delhi), Russia (Moscow)
                Africa: Egypt (Cairo), Nigeria (Abuja), South Africa (Cape Town/Pretoria/Bloemfontein)
                Oceania: Australia (Canberra), New Zealand (Wellington)''',
                'keywords': ['countries', 'capitals', 'geography', 'continents', 'cities', 'nations'],
                'difficulty_level': 'beginner',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.95
            },
            
            # Writing and Grammar Knowledge
            {
                'id': 'writing_001',
                'topic': 'English Grammar Fundamentals',
                'category': 'writing',
                'content': '''English Grammar Basics:
                Parts of Speech: Noun, Verb, Adjective, Adverb, Pronoun, Preposition, Conjunction, Interjection
                Sentence Structure: Subject + Predicate, Simple/Compound/Complex sentences
                Verb Tenses: Present (I walk), Past (I walked), Future (I will walk), Perfect tenses
                Punctuation: Period (.), Comma (,), Semicolon (;), Colon (:), Question mark (?), Exclamation (!)
                Common Errors: Subject-verb agreement, dangling modifiers, comma splices, sentence fragments''',
                'keywords': ['grammar', 'english', 'sentence', 'verb', 'noun', 'punctuation', 'tenses'],
                'difficulty_level': 'beginner',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.93
            },
            
            # Mathematics Knowledge
            {
                'id': 'math_001',
                'topic': 'Basic Algebra',
                'category': 'mathematics',
                'content': '''Algebra Fundamentals:
                Variables: Letters representing unknown values (x, y, z)
                Equations: Mathematical statements with equals sign (2x + 3 = 7)
                Operations: Addition (+), Subtraction (-), Multiplication (×), Division (÷), Exponentiation (^)
                Solving equations: Isolate variable using inverse operations
                Factoring: Breaking expressions into products (x² - 4 = (x+2)(x-2))
                Quadratic Formula: x = [-b ± √(b²-4ac)] / 2a for ax² + bx + c = 0''',
                'keywords': ['algebra', 'equations', 'variables', 'solving', 'quadratic', 'factoring'],
                'difficulty_level': 'intermediate',
                'source': 'Built-in Knowledge',
                'confidence_score': 0.91
            }
        ]
        
        # Insert default knowledge if database is empty
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM knowledge_items')
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📚 Loading default knowledge base...")
            for item in default_knowledge:
                self.add_knowledge_item(
                    KnowledgeItem(
                        id=item['id'],
                        topic=item['topic'],
                        category=item['category'],
                        content=item['content'],
                        keywords=item['keywords'],
                        difficulty_level=item['difficulty_level'],
                        last_updated=datetime.now(),
                        source=item['source'],
                        confidence_score=item['confidence_score']
                    )
                )
            print(f"✅ Loaded {len(default_knowledge)} knowledge items")
        
        conn.close()
    
    def add_knowledge_item(self, item: KnowledgeItem) -> bool:
        """Add a new knowledge item to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO knowledge_items 
                (id, topic, category, content, keywords, difficulty_level, last_updated, source, confidence_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.id, item.topic, item.category, item.content,
                json.dumps(item.keywords), item.difficulty_level,
                item.last_updated.isoformat(), item.source, item.confidence_score
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error adding knowledge item: {e}")
            return False
    
    def analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """Analyze user query to determine intent and extract key information"""
        query_lower = query.lower().strip()
        
        intent_patterns = {
            'question': ['what', 'how', 'why', 'when', 'where', 'who', 'which', '?'],
            'definition': ['define', 'meaning', 'what is', 'what are'],
            'explanation': ['explain', 'describe', 'tell me about'],
            'comparison': ['compare', 'difference', 'versus', 'vs', 'better'],
            'calculation': ['calculate', 'solve', 'compute', 'math', '=', '+', '-', '*', '/'],
            'grammar_check': ['grammar', 'correct', 'check', 'fix', 'proofread'],
            'paraphrase': ['paraphrase', 'rephrase', 'rewrite', 'different way'],
            'coding': ['code', 'program', 'function', 'algorithm', 'debug'],
            'history': ['history', 'historical', 'when did', 'ancient', 'past'],
            'geography': ['where is', 'location', 'country', 'city', 'capital'],
            'politics': ['government', 'political', 'policy', 'election', 'democracy']
        }
        
        detected_intents = []
        confidence_scores = {}
        
        for intent, patterns in intent_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in query_lower)
            if matches > 0:
                confidence = min(matches / len(patterns), 1.0)
                detected_intents.append(intent)
                confidence_scores[intent] = confidence
        
        # Primary intent is the one with highest confidence
        primary_intent = max(confidence_scores.keys(), key=lambda x: confidence_scores[x]) if confidence_scores else 'general'
        
        # Extract key entities using NLP if available
        entities = self._extract_entities(query)
        
        return {
            'primary_intent': primary_intent,
            'all_intents': detected_intents,
            'confidence_scores': confidence_scores,
            'entities': entities,
            'query_length': len(query.split()),
            'complexity': self._assess_query_complexity(query)
        }
    
    def _extract_entities(self, query: str) -> List[Dict[str, str]]:
        """Extract named entities from query using NLP"""
        entities = []
        
        if self.nlp_processor:
            doc = self.nlp_processor(query)
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'description': spacy.explain(ent.label_)
                })
        
        return entities
    
    def _assess_query_complexity(self, query: str) -> str:
        """Assess the complexity of a user query"""
        words = query.split()
        
        complexity_indicators = {
            'simple': len(words) <= 5,
            'medium': 5 < len(words) <= 15,
            'complex': len(words) > 15
        }
        
        # Check for complex concepts
        complex_terms = ['analyze', 'evaluate', 'synthesize', 'compare', 'contrast', 'critique']
        has_complex_terms = any(term in query.lower() for term in complex_terms)
        
        if has_complex_terms or len(words) > 20:
            return 'complex'
        elif len(words) > 10 or '?' in query:
            return 'medium'
        else:
            return 'simple'
    
    def search_knowledge(self, query: str, limit: int = 5) -> QueryResult:
        """Search knowledge base for relevant information"""
        query_analysis = self.analyze_query_intent(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build search query based on intent
        search_terms = self._extract_search_terms(query)
        
        # Search in content and keywords
        search_query = '''
            SELECT * FROM knowledge_items 
            WHERE content LIKE ? OR keywords LIKE ? OR topic LIKE ?
            ORDER BY confidence_score DESC
            LIMIT ?
        '''
        
        search_pattern = f"%{' '.join(search_terms)}%"
        cursor.execute(search_query, (search_pattern, search_pattern, search_pattern, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert results to KnowledgeItem objects
        knowledge_items = []
        for row in results:
            item = KnowledgeItem(
                id=row[0],
                topic=row[1],
                category=row[2],
                content=row[3],
                keywords=json.loads(row[4]),
                difficulty_level=row[5],
                last_updated=datetime.fromisoformat(row[6]),
                source=row[7],
                confidence_score=row[8]
            )
            knowledge_items.append(item)
        
        # Generate suggested actions based on intent
        suggested_actions = self._generate_suggested_actions(query_analysis)
        
        return QueryResult(
            items=knowledge_items,
            total_score=sum(item.confidence_score for item in knowledge_items),
            query_intent=query_analysis['primary_intent'],
            suggested_actions=suggested_actions
        )
    
    def _extract_search_terms(self, query: str) -> List[str]:
        """Extract meaningful search terms from query"""
        terms = []
        
        if self.lemmatizer and self.stop_words:
            # Use NLTK for better term extraction
            tokens = word_tokenize(query.lower())
            terms = [self.lemmatizer.lemmatize(token) for token in tokens 
                    if token not in self.stop_words and token.isalpha()]
        else:
            # Simple word extraction
            terms = [word.lower() for word in query.split() 
                    if len(word) > 2 and word.isalpha()]
        
        return terms
    
    def _generate_suggested_actions(self, query_analysis: Dict) -> List[str]:
        """Generate suggested actions based on query analysis"""
        intent = query_analysis['primary_intent']
        
        action_map = {
            'question': ['Search knowledge base', 'Ask for clarification', 'Provide examples'],
            'definition': ['Look up definition', 'Provide examples', 'Explain context'],
            'explanation': ['Provide detailed explanation', 'Give examples', 'Show related topics'],
            'calculation': ['Perform calculation', 'Show step-by-step solution', 'Verify result'],
            'grammar_check': ['Check grammar', 'Suggest corrections', 'Explain rules'],
            'paraphrase': ['Provide alternatives', 'Suggest synonyms', 'Improve style'],
            'coding': ['Provide code examples', 'Explain concepts', 'Debug issues'],
            'comparison': ['Compare items', 'List differences', 'Highlight similarities']
        }
        
        return action_map.get(intent, ['Provide general information', 'Search knowledge base'])
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total items
        cursor.execute('SELECT COUNT(*) FROM knowledge_items')
        total_items = cursor.fetchone()[0]
        
        # Items by category
        cursor.execute('SELECT category, COUNT(*) FROM knowledge_items GROUP BY category')
        category_counts = dict(cursor.fetchall())
        
        # Items by difficulty
        cursor.execute('SELECT difficulty_level, COUNT(*) FROM knowledge_items GROUP BY difficulty_level')
        difficulty_counts = dict(cursor.fetchall())
        
        # Average confidence score
        cursor.execute('SELECT AVG(confidence_score) FROM knowledge_items')
        avg_confidence = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_items': total_items,
            'categories': category_counts,
            'difficulty_levels': difficulty_counts,
            'average_confidence': round(avg_confidence, 2),
            'last_updated': datetime.now().isoformat()
        }

class GrammarChecker:
    """Advanced grammar checking and correction service"""
    
    def __init__(self):
        self.initialized = False
        self._init_grammar_tools()
    
    def _init_grammar_tools(self):
        """Initialize grammar checking tools"""
        if HAS_TEXTBLOB:
            self.initialized = True
            print("✅ Grammar checker initialized with TextBlob")
    
    def check_grammar(self, text: str) -> Dict[str, Any]:
        """Check grammar and suggest corrections"""
        if not self.initialized:
            return {
                'original': text,
                'corrected': text,
                'errors': [],
                'suggestions': ['Grammar checker not available - install TextBlob'],
                'confidence': 0.0
            }
        
        try:
            blob = TextBlob(text)
            corrected = str(blob.correct())
            
            # Simple error detection
            errors = []
            if text != corrected:
                errors.append({
                    'type': 'spelling/grammar',
                    'original': text,
                    'suggestion': corrected,
                    'confidence': 0.8
                })
            
            return {
                'original': text,
                'corrected': corrected,
                'errors': errors,
                'suggestions': self._generate_style_suggestions(text),
                'confidence': 0.9 if text == corrected else 0.7
            }
        
        except Exception as e:
            return {
                'original': text,
                'corrected': text,
                'errors': [{'type': 'error', 'message': str(e)}],
                'suggestions': [],
                'confidence': 0.0
            }
    
    def _generate_style_suggestions(self, text: str) -> List[str]:
        """Generate writing style suggestions"""
        suggestions = []
        
        # Check sentence length
        sentences = text.split('.')
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        if long_sentences:
            suggestions.append("Consider breaking up long sentences for better readability")
        
        # Check passive voice (simple detection)
        if ' was ' in text or ' were ' in text:
            suggestions.append("Consider using active voice for stronger writing")
        
        # Check repetitive words
        words = text.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 4:  # Only check longer words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        repeated = [word for word, count in word_counts.items() if count > 3]
        if repeated:
            suggestions.append(f"Consider synonyms for repeated words: {', '.join(repeated)}")
        
        return suggestions

class MathCalculator:
    """Advanced mathematical calculation service"""
    
    def __init__(self):
        self.has_sympy = HAS_SYMPY
        self.has_numpy = HAS_NUMPY
        
        if self.has_sympy:
            print("✅ Mathematical calculator initialized with SymPy")
    
    def solve_equation(self, equation: str) -> Dict[str, Any]:
        """Solve mathematical equations"""
        if not self.has_sympy:
            return {
                'input': equation,
                'result': 'Mathematical solver not available - install SymPy',
                'steps': [],
                'type': 'error'
            }
        
        try:
            # Parse equation
            if '=' in equation:
                left, right = equation.split('=')
                expr = sp.sympify(left) - sp.sympify(right)
            else:
                expr = sp.sympify(equation)
            
            # Find symbols
            symbols_in_expr = list(expr.free_symbols)
            
            if symbols_in_expr:
                # Solve for variables
                solutions = solve(expr, symbols_in_expr[0])
                return {
                    'input': equation,
                    'result': solutions,
                    'steps': [f"Solving for {symbols_in_expr[0]}", f"Solutions: {solutions}"],
                    'type': 'algebraic'
                }
            else:
                # Evaluate expression
                result = float(expr.evalf())
                return {
                    'input': equation,
                    'result': result,
                    'steps': [f"Evaluating: {equation}", f"Result: {result}"],
                    'type': 'arithmetic'
                }
        
        except Exception as e:
            return {
                'input': equation,
                'result': f'Error: {str(e)}',
                'steps': ['Unable to parse mathematical expression'],
                'type': 'error'
            }
    
    def calculate_derivatives(self, function: str, variable: str = 'x') -> Dict[str, Any]:
        """Calculate derivatives of mathematical functions"""
        if not self.has_sympy:
            return {'error': 'SymPy not available'}
        
        try:
            x = symbols(variable)
            expr = sp.sympify(function)
            derivative = diff(expr, x)
            
            return {
                'function': function,
                'variable': variable,
                'derivative': str(derivative),
                'simplified': str(simplify(derivative)),
                'type': 'calculus'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_integrals(self, function: str, variable: str = 'x') -> Dict[str, Any]:
        """Calculate integrals of mathematical functions"""
        if not self.has_sympy:
            return {'error': 'SymPy not available'}
        
        try:
            x = symbols(variable)
            expr = sp.sympify(function)
            integral = integrate(expr, x)
            
            return {
                'function': function,
                'variable': variable,
                'integral': str(integral),
                'type': 'calculus'
            }
        except Exception as e:
            return {'error': str(e)}

# Initialize global instances
knowledge_base = KnowledgeBaseService()
grammar_checker = GrammarChecker()
math_calculator = MathCalculator()

def get_knowledge_response(query: str) -> str:
    """Main function to get knowledge-based responses"""
    try:
        # Search knowledge base
        results = knowledge_base.search_knowledge(query)
        
        if not results.items:
            return f"I don't have specific information about that topic in my knowledge base yet. Let me help you with what I do know or suggest where you might find more information."
        
        # Format response based on intent
        if results.query_intent == 'calculation':
            # Handle math calculations
            math_result = math_calculator.solve_equation(query)
            if math_result['type'] != 'error':
                return f"**Mathematical Solution:**\n{math_result['result']}\n\n**Steps:**\n" + "\n".join(math_result['steps'])
        
        # Standard knowledge response
        best_match = results.items[0]
        response = f"**{best_match.topic}** ({best_match.category.title()})\n\n"
        response += best_match.content[:500] + ("..." if len(best_match.content) > 500 else "")
        
        if len(results.items) > 1:
            response += f"\n\n**Related Topics:** {', '.join([item.topic for item in results.items[1:3]])}"
        
        return response
        
    except Exception as e:
        return f"I encountered an issue while searching my knowledge base: {str(e)}"

if __name__ == "__main__":
    # Test the knowledge base system
    print("🧠 Clang Advanced Knowledge Base System")
    print("=" * 50)
    
    # Display stats
    stats = knowledge_base.get_knowledge_stats()
    print(f"📊 Knowledge Base Stats:")
    print(f"  Total Items: {stats['total_items']}")
    print(f"  Categories: {', '.join(stats['categories'].keys())}")
    print(f"  Average Confidence: {stats['average_confidence']}")
    
    # Test queries
    test_queries = [
        "What is Python programming?",
        "Explain World War 2",
        "What is the capital of France?",
        "How do I write good grammar?",
        "Solve x^2 + 5x + 6 = 0"
    ]
    
    print(f"\n🔍 Testing Knowledge Queries:")
    for query in test_queries:
        print(f"\nQ: {query}")
        response = get_knowledge_response(query)
        print(f"A: {response[:200]}...")
