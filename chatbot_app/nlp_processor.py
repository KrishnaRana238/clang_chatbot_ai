"""
Advanced NLP Processing Service for Clang AI
Comprehensive natural language processing and understanding
"""

import re
import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

# Try to import advanced NLP libraries
try:
    import spacy
    from spacy.matcher import Matcher
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False

try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.chunk import ne_chunk
    from nltk.tag import pos_tag
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

@dataclass
class NLPAnalysis:
    """Complete NLP analysis result"""
    original_text: str
    tokens: List[str]
    sentences: List[str]
    pos_tags: List[Tuple[str, str]]
    named_entities: List[Dict[str, str]]
    sentiment: Dict[str, float]
    intent: str
    confidence: float
    complexity_score: float
    language_detected: str
    readability_score: float

@dataclass
class ParaphraseResult:
    """Paraphrasing result with alternatives"""
    original: str
    paraphrases: List[str]
    style_variations: List[str]
    confidence: float

class AdvancedNLPProcessor:
    """Comprehensive Natural Language Processing Service"""
    
    def __init__(self):
        self.nlp_model = None
        self.matcher = None
        self.sentiment_analyzer = None
        self.language_patterns = {}
        
        self._initialize_nlp_components()
        self._load_language_patterns()
    
    def _initialize_nlp_components(self):
        """Initialize all NLP processing components"""
        
        # Initialize spaCy
        if HAS_SPACY:
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
                self.matcher = Matcher(self.nlp_model.vocab)
                self._setup_custom_patterns()
                print("✅ SpaCy NLP model loaded successfully")
            except OSError:
                print("⚠️  SpaCy model not found. Install with: python -m spacy download en_core_web_sm")
        
        # Initialize NLTK components
        if HAS_NLTK:
            try:
                nltk.download('vader_lexicon', quiet=True)
                nltk.download('punkt', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                nltk.download('maxent_ne_chunker', quiet=True)
                nltk.download('words', quiet=True)
                
                self.sentiment_analyzer = SentimentIntensityAnalyzer()
                print("✅ NLTK components initialized")
            except Exception as e:
                print(f"⚠️  NLTK initialization failed: {e}")
    
    def _setup_custom_patterns(self):
        """Setup custom patterns for entity recognition"""
        if not self.matcher:
            return
        
        # Programming concepts pattern
        programming_pattern = [{"LOWER": {"IN": ["function", "class", "variable", "loop", "array", "object"]}}]
        self.matcher.add("PROGRAMMING_CONCEPT", [programming_pattern])
        
        # Mathematical expressions
        math_pattern = [{"IS_ALPHA": False}, {"TEXT": {"REGEX": r"[+\-*/=]"}}, {"IS_ALPHA": False}]
        self.matcher.add("MATH_EXPRESSION", [math_pattern])
        
        # Question patterns
        question_pattern = [{"LOWER": {"IN": ["what", "how", "why", "when", "where", "who", "which"]}}]
        self.matcher.add("QUESTION_WORD", [question_pattern])
    
    def _load_language_patterns(self):
        """Load language patterns for intent recognition"""
        self.language_patterns = {
            "coding_request": [
                r"\b(write|create|generate|make)\s+(code|program|function|script)",
                r"\b(how\s+to\s+code|programming\s+help|coding\s+problem)",
                r"\b(debug|fix\s+code|error\s+in\s+code)"
            ],
            "math_problem": [
                r"\b(solve|calculate|compute|find)\s+",
                r"[+\-*/=]\s*\d+",
                r"\b(equation|formula|derivative|integral)",
                r"\d+\s*[+\-*/]\s*\d+"
            ],
            "grammar_check": [
                r"\b(check|correct|fix)\s+(grammar|spelling|writing)",
                r"\b(proofread|edit|review)\s+",
                r"is\s+this\s+(correct|right|proper)"
            ],
            "explanation_request": [
                r"\b(explain|describe|tell\s+me\s+about|what\s+is)",
                r"\b(how\s+does|why\s+does|what\s+happens)",
                r"\b(define|meaning\s+of|definition)"
            ],
            "comparison_request": [
                r"\b(compare|difference|versus|vs\.?|better)",
                r"\b(similar|different|alike|contrast)",
                r"\b(pros\s+and\s+cons|advantages|disadvantages)"
            ]
        }
    
    async def analyze_text(self, text: str) -> NLPAnalysis:
        """Perform comprehensive NLP analysis"""
        
        # Basic tokenization
        tokens = self._tokenize(text)
        sentences = self._sentence_tokenize(text)
        
        # POS tagging
        pos_tags = self._get_pos_tags(text)
        
        # Named entity recognition
        named_entities = self._extract_named_entities(text)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(text)
        
        # Intent classification
        intent, confidence = self._classify_intent(text)
        
        # Complexity scoring
        complexity_score = self._calculate_complexity(text)
        
        # Language detection
        language = self._detect_language(text)
        
        # Readability scoring
        readability = self._calculate_readability(text)
        
        return NLPAnalysis(
            original_text=text,
            tokens=tokens,
            sentences=sentences,
            pos_tags=pos_tags,
            named_entities=named_entities,
            sentiment=sentiment,
            intent=intent,
            confidence=confidence,
            complexity_score=complexity_score,
            language_detected=language,
            readability_score=readability
        )
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        if HAS_NLTK:
            return word_tokenize(text)
        else:
            # Simple tokenization
            return re.findall(r'\b\w+\b', text.lower())
    
    def _sentence_tokenize(self, text: str) -> List[str]:
        """Split text into sentences"""
        if HAS_NLTK:
            return sent_tokenize(text)
        else:
            # Simple sentence splitting
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]
    
    def _get_pos_tags(self, text: str) -> List[Tuple[str, str]]:
        """Get part-of-speech tags"""
        if HAS_NLTK:
            tokens = word_tokenize(text)
            return pos_tag(tokens)
        else:
            tokens = self._tokenize(text)
            return [(token, 'UNKNOWN') for token in tokens]
    
    def _extract_named_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities from text"""
        entities = []
        
        if self.nlp_model:
            doc = self.nlp_model(text)
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'description': spacy.explain(ent.label_) if ent.label_ else 'Unknown',
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        
        elif HAS_NLTK:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            chunks = ne_chunk(pos_tags)
            
            for chunk in chunks:
                if hasattr(chunk, 'label'):
                    entity_text = ' '.join([token for token, pos in chunk])
                    entities.append({
                        'text': entity_text,
                        'label': chunk.label(),
                        'description': chunk.label(),
                        'start': 0,
                        'end': 0
                    })
        
        return entities
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of the text"""
        if self.sentiment_analyzer:
            scores = self.sentiment_analyzer.polarity_scores(text)
            return {
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu'],
                'compound': scores['compound']
            }
        elif HAS_TEXTBLOB:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            return {
                'positive': max(0, polarity),
                'negative': max(0, -polarity),
                'neutral': 1 - abs(polarity),
                'compound': polarity
            }
        else:
            return {
                'positive': 0.5,
                'negative': 0.0,
                'neutral': 0.5,
                'compound': 0.0
            }
    
    def _classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify the intent of the text"""
        text_lower = text.lower()
        
        intent_scores = {}
        
        for intent, patterns in self.language_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            if score > 0:
                intent_scores[intent] = score / len(patterns)
        
        if not intent_scores:
            return "general_query", 0.5
        
        best_intent = max(intent_scores.keys(), key=lambda x: intent_scores[x])
        confidence = min(intent_scores[best_intent], 1.0)
        
        return best_intent, confidence
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score (0-1)"""
        factors = {
            'word_count': len(text.split()),
            'sentence_count': len(self._sentence_tokenize(text)),
            'avg_word_length': sum(len(word) for word in text.split()) / max(1, len(text.split())),
            'punctuation_ratio': len([c for c in text if c in '.,;:!?']) / max(1, len(text)),
            'capital_ratio': len([c for c in text if c.isupper()]) / max(1, len(text))
        }
        
        # Normalize and weight factors
        complexity = 0
        complexity += min(factors['word_count'] / 100, 1.0) * 0.3
        complexity += min(factors['avg_word_length'] / 10, 1.0) * 0.3
        complexity += min(factors['punctuation_ratio'] * 10, 1.0) * 0.2
        complexity += min(factors['sentence_count'] / 20, 1.0) * 0.2
        
        return min(complexity, 1.0)
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection (primarily English focus)"""
        # Simple heuristic for English detection
        english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        words = text.lower().split()
        english_count = sum(1 for word in words if word in english_words)
        
        if english_count / max(1, len(words)) > 0.1:
            return 'english'
        else:
            return 'unknown'
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score (Flesch-like)"""
        words = text.split()
        sentences = self._sentence_tokenize(text)
        
        if not words or not sentences:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables = self._estimate_syllables(text) / len(words)
        
        # Simplified Flesch formula
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
        
        # Normalize to 0-1 scale
        return max(0, min(100, readability)) / 100
    
    def _estimate_syllables(self, text: str) -> int:
        """Estimate syllable count in text"""
        words = text.split()
        total_syllables = 0
        
        for word in words:
            word_lower = word.lower().strip('.,!?;:')
            syllables = len(re.findall(r'[aeiouAEIOU]', word_lower))
            if syllables == 0:
                syllables = 1  # Every word has at least one syllable
            total_syllables += syllables
        
        return total_syllables
    
    async def paraphrase_text(self, text: str, style: str = 'neutral') -> ParaphraseResult:
        """Generate paraphrases and style variations of text"""
        
        # Basic paraphrasing using synonym replacement
        paraphrases = []
        style_variations = []
        
        if HAS_TEXTBLOB:
            try:
                blob = TextBlob(text)
                
                # Simple synonym replacement
                words = blob.words
                paraphrase_candidates = []
                
                for i, word in enumerate(words):
                    synonyms = word.synsets
                    if synonyms:
                        # Get first synonym from first synset
                        synonym = synonyms[0].lemmas()[0].name()
                        if synonym != word and '_' not in synonym:
                            new_words = list(words)
                            new_words[i] = synonym
                            paraphrase_candidates.append(' '.join(new_words))
                
                paraphrases = paraphrase_candidates[:3]  # Top 3
                
            except Exception as e:
                paraphrases = [f"Paraphrasing failed: {e}"]
        
        # Generate style variations
        style_variations = self._generate_style_variations(text, style)
        
        return ParaphraseResult(
            original=text,
            paraphrases=paraphrases if paraphrases else [text],
            style_variations=style_variations,
            confidence=0.7 if paraphrases else 0.3
        )
    
    def _generate_style_variations(self, text: str, style: str) -> List[str]:
        """Generate different style variations"""
        variations = []
        
        if style == 'formal':
            # Make more formal
            formal_text = text.replace("don't", "do not").replace("won't", "will not")
            formal_text = formal_text.replace("can't", "cannot").replace("isn't", "is not")
            variations.append(formal_text)
        
        elif style == 'casual':
            # Make more casual
            casual_text = text.replace("do not", "don't").replace("will not", "won't")
            casual_text = casual_text.replace("cannot", "can't").replace("is not", "isn't")
            variations.append(casual_text)
        
        elif style == 'academic':
            # Academic style
            academic = f"This analysis demonstrates that {text.lower()}"
            variations.append(academic)
        
        elif style == 'creative':
            # Creative style
            creative = f"Imagine if {text.lower()} - wouldn't that be fascinating?"
            variations.append(creative)
        
        return variations
    
    def extract_key_phrases(self, text: str, max_phrases: int = 5) -> List[Dict[str, Any]]:
        """Extract key phrases from text"""
        key_phrases = []
        
        if self.nlp_model:
            doc = self.nlp_model(text)
            
            # Extract noun phrases
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) >= 2:  # Multi-word phrases
                    key_phrases.append({
                        'text': chunk.text,
                        'type': 'noun_phrase',
                        'importance': len(chunk.text.split()) / 10,  # Longer = more important
                        'pos': 'NOUN'
                    })
            
            # Extract entities as key phrases
            for ent in doc.ents:
                key_phrases.append({
                    'text': ent.text,
                    'type': 'named_entity',
                    'importance': 0.8,
                    'pos': ent.label_
                })
        
        else:
            # Fallback: extract capitalized phrases and long words
            words = text.split()
            for i, word in enumerate(words):
                if word[0].isupper() and len(word) > 5:
                    key_phrases.append({
                        'text': word,
                        'type': 'important_word',
                        'importance': len(word) / 20,
                        'pos': 'UNKNOWN'
                    })
        
        # Sort by importance and return top phrases
        key_phrases.sort(key=lambda x: x['importance'], reverse=True)
        return key_phrases[:max_phrases]
    
    def detect_question_type(self, text: str) -> Dict[str, Any]:
        """Detect the type of question being asked"""
        text_lower = text.lower().strip()
        
        question_types = {
            'what': ['what', 'what is', 'what are', 'what does'],
            'how': ['how', 'how to', 'how do', 'how does', 'how can'],
            'why': ['why', 'why is', 'why does', 'why do'],
            'when': ['when', 'when is', 'when does', 'when did'],
            'where': ['where', 'where is', 'where does', 'where can'],
            'who': ['who', 'who is', 'who are', 'who does'],
            'which': ['which', 'which is', 'which are', 'which one'],
            'yes_no': ['is', 'are', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can'],
            'choice': ['or', 'versus', 'vs', 'better', 'prefer'],
            'definition': ['define', 'meaning', 'means', 'definition of'],
            'explanation': ['explain', 'describe', 'tell me about'],
            'comparison': ['compare', 'difference', 'similar', 'contrast']
        }
        
        detected_types = []
        confidence_scores = {}
        
        for q_type, patterns in question_types.items():
            for pattern in patterns:
                if pattern in text_lower:
                    if q_type not in detected_types:
                        detected_types.append(q_type)
                        confidence_scores[q_type] = confidence_scores.get(q_type, 0) + 1
        
        # Check for question mark
        has_question_mark = '?' in text
        
        # Determine primary question type
        if confidence_scores:
            primary_type = max(confidence_scores.keys(), key=lambda x: confidence_scores[x])
            confidence = min(confidence_scores[primary_type] / 3, 1.0)
        else:
            primary_type = 'general' if has_question_mark else 'statement'
            confidence = 0.5 if has_question_mark else 0.3
        
        return {
            'primary_type': primary_type,
            'all_types': detected_types,
            'confidence': confidence,
            'has_question_mark': has_question_mark,
            'is_question': has_question_mark or bool(detected_types)
        }

# Global NLP processor instance
nlp_processor = AdvancedNLPProcessor()

async def process_user_query(query: str) -> Dict[str, Any]:
    """Main function to process user queries with full NLP analysis"""
    
    # Perform comprehensive NLP analysis
    analysis = await nlp_processor.analyze_text(query)
    
    # Detect question type
    question_info = nlp_processor.detect_question_type(query)
    
    # Extract key phrases
    key_phrases = nlp_processor.extract_key_phrases(query)
    
    # Generate response strategy based on analysis
    response_strategy = {
        'should_search_knowledge': analysis.intent in ['explanation_request', 'comparison_request'],
        'should_calculate': analysis.intent == 'math_problem',
        'should_check_grammar': analysis.intent == 'grammar_check',
        'should_paraphrase': 'paraphrase' in query.lower() or 'rephrase' in query.lower(),
        'should_provide_code': analysis.intent == 'coding_request',
        'complexity_level': 'high' if analysis.complexity_score > 0.7 else 'medium' if analysis.complexity_score > 0.4 else 'low'
    }
    
    return {
        'analysis': analysis,
        'question_info': question_info,
        'key_phrases': key_phrases,
        'response_strategy': response_strategy,
        'processing_time': datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Test the NLP processor
    print("🧠 Clang Advanced NLP Processor")
    print("=" * 40)
    
    test_queries = [
        "What is machine learning and how does it work?",
        "Can you help me debug this Python code?",
        "Solve the equation x^2 + 5x + 6 = 0",
        "Please check the grammar in this sentence: 'Me and him went to the store.'",
        "Compare the advantages of Python versus JavaScript for web development"
    ]
    
    async def test_nlp():
        for query in test_queries:
            print(f"\nQuery: {query}")
            result = await process_user_query(query)
            print(f"Intent: {result['analysis'].intent} (confidence: {result['analysis'].confidence:.2f})")
            print(f"Question Type: {result['question_info']['primary_type']}")
            print(f"Complexity: {result['response_strategy']['complexity_level']}")
            print(f"Key Phrases: {[p['text'] for p in result['key_phrases'][:3]]}")
    
    asyncio.run(test_nlp())
