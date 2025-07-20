"""
Admin and diagnostic views for Enhanced Clang AI
Provides system information, capabilities overview, and testing interface
"""

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import asyncio

# Import enhanced services
try:
    from .enhanced_clang_service import enhanced_clang, get_clang_response
    from .knowledge_base_service import knowledge_base, grammar_checker, math_calculator
    from .nlp_processor import nlp_processor
    HAS_ENHANCED_SERVICES = True
except ImportError:
    HAS_ENHANCED_SERVICES = False

@api_view(['GET'])
def system_capabilities(request):
    """Get comprehensive system capabilities and statistics"""
    
    if not HAS_ENHANCED_SERVICES:
        return Response({
            'error': 'Enhanced services not available',
            'basic_info': {
                'name': 'Clang Basic',
                'version': '1.0',
                'status': 'fallback_mode'
            }
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        # Get capabilities info
        capabilities = enhanced_clang.get_capabilities_info()
        
        # Get knowledge base stats
        kb_stats = knowledge_base.get_knowledge_stats()
        
        return Response({
            'system_info': {
                'name': capabilities['name'],
                'version': capabilities['version'],
                'status': 'fully_operational',
                'enhanced_services': True
            },
            'core_capabilities': capabilities['core_capabilities'],
            'supported_topics': capabilities['supported_topics'],
            'knowledge_base': {
                'total_items': kb_stats['total_items'],
                'categories': kb_stats['categories'],
                'difficulty_levels': kb_stats['difficulty_levels'],
                'average_confidence': kb_stats['average_confidence']
            },
            'session_statistics': capabilities['session_statistics'],
            'nlp_features': {
                'sentiment_analysis': True,
                'intent_recognition': True,
                'entity_extraction': True,
                'complexity_assessment': True,
                'paraphrasing': True
            },
            'mathematical_capabilities': {
                'equation_solving': True,
                'calculus': True,
                'symbolic_math': True,
                'numerical_computation': True
            },
            'language_features': {
                'grammar_checking': True,
                'style_analysis': True,
                'writing_assistance': True,
                'error_correction': True
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Failed to get system info: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])  
def test_capabilities(request):
    """Test specific capabilities with sample inputs"""
    
    if not HAS_ENHANCED_SERVICES:
        return Response({
            'error': 'Enhanced services not available'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    test_queries = {
        'knowledge_base': "What is Python programming?",
        'mathematics': "Solve x^2 + 5x + 6 = 0",
        'grammar_check': "check grammar: Me and him went to the store yesterday.",
        'coding_help': "Write a Python function to calculate fibonacci numbers",
        'paraphrasing': "paraphrase: The weather is very nice today",
        'complex_analysis': "Compare the advantages and disadvantages of Python versus JavaScript for web development"
    }
    
    # Allow custom test query
    custom_query = request.data.get('query')
    if custom_query:
        test_queries['custom'] = custom_query
    
    results = {}
    
    async def run_tests():
        for test_name, query in test_queries.items():
            try:
                print(f"🔍 Testing {test_name}: {query}")
                result = await get_clang_response(query)
                
                results[test_name] = {
                    'query': query,
                    'response': result['response'][:300] + "..." if len(result['response']) > 300 else result['response'],
                    'full_response_length': len(result['response']),
                    'metadata': {
                        'intent': result['metadata'].get('intent'),
                        'confidence': result['metadata'].get('confidence'),
                        'complexity': result['metadata'].get('complexity'),
                        'processing_time': result['metadata'].get('processing_time_seconds'),
                        'capabilities_used': result['metadata'].get('capabilities_activated', [])
                    },
                    'success': True
                }
            except Exception as e:
                results[test_name] = {
                    'query': query,
                    'error': str(e),
                    'success': False
                }
    
    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_tests())
    finally:
        loop.close()
    
    return Response({
        'test_results': results,
        'summary': {
            'total_tests': len(test_queries),
            'successful_tests': sum(1 for r in results.values() if r.get('success', False)),
            'failed_tests': sum(1 for r in results.values() if not r.get('success', False))
        }
    })

@api_view(['POST'])
def analyze_text(request):
    """Perform detailed NLP analysis on provided text"""
    
    if not HAS_ENHANCED_SERVICES:
        return Response({
            'error': 'NLP analysis not available'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    text = request.data.get('text', '')
    if not text:
        return Response({
            'error': 'No text provided for analysis'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    async def perform_analysis():
        try:
            # Perform comprehensive NLP analysis
            analysis = await nlp_processor.analyze_text(text)
            
            # Extract key phrases
            key_phrases = nlp_processor.extract_key_phrases(text)
            
            # Detect question type if applicable
            question_info = nlp_processor.detect_question_type(text)
            
            return {
                'text_analysis': {
                    'original_text': analysis.original_text,
                    'word_count': len(analysis.tokens),
                    'sentence_count': len(analysis.sentences),
                    'language_detected': analysis.language_detected,
                    'complexity_score': analysis.complexity_score,
                    'readability_score': analysis.readability_score
                },
                'linguistic_features': {
                    'tokens': analysis.tokens[:20],  # First 20 tokens
                    'sentences': analysis.sentences,
                    'pos_tags': analysis.pos_tags[:20],  # First 20 POS tags
                    'named_entities': analysis.named_entities
                },
                'semantic_analysis': {
                    'intent': analysis.intent,
                    'confidence': analysis.confidence,
                    'sentiment': analysis.sentiment,
                    'key_phrases': [p['text'] for p in key_phrases]
                },
                'question_analysis': {
                    'is_question': question_info['is_question'],
                    'question_type': question_info['primary_type'],
                    'question_confidence': question_info['confidence'],
                    'detected_types': question_info['all_types']
                }
            }
            
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    # Run analysis
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(perform_analysis())
    finally:
        loop.close()
    
    if 'error' in result:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(result)

@api_view(['GET'])
def demo_interface(request):
    """Render a demo interface for testing Clang's capabilities"""
    
    return render(request, 'demo.html', {
        'has_enhanced_services': HAS_ENHANCED_SERVICES,
        'demo_queries': [
            "What is machine learning?",
            "Solve the equation 2x + 5 = 13", 
            "Write a Python function to sort a list",
            "Check grammar: Their going to the store.",
            "Explain the causes of World War II",
            "What is the capital of Japan?",
            "Compare Python and JavaScript",
            "Paraphrase: The quick brown fox jumps over the lazy dog"
        ]
    })

@api_view(['POST'])
def math_solver(request):
    """Dedicated mathematical problem solver"""
    
    if not HAS_ENHANCED_SERVICES:
        return Response({
            'error': 'Mathematical solver not available'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    equation = request.data.get('equation', '')
    if not equation:
        return Response({
            'error': 'No equation provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Solve equation
        result = math_calculator.solve_equation(equation)
        
        # Also try derivatives and integrals if it's a function
        additional_analysis = {}
        if result['type'] != 'error' and any(var in equation for var in ['x', 'y', 'z']):
            try:
                derivative = math_calculator.calculate_derivatives(equation)
                if 'error' not in derivative:
                    additional_analysis['derivative'] = derivative
                
                integral = math_calculator.calculate_integrals(equation)
                if 'error' not in integral:
                    additional_analysis['integral'] = integral
            except:
                pass  # Skip additional analysis if it fails
        
        return Response({
            'equation': equation,
            'solution': result,
            'additional_analysis': additional_analysis,
            'success': result['type'] != 'error'
        })
        
    except Exception as e:
        return Response({
            'equation': equation,
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
