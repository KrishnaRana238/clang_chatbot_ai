"""
API Testing endpoint to verify all API providers in production
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_all_apis():
    """Test all API providers to see which ones are working"""
    results = {}
    
    # Test Cohere
    try:
        import cohere
        cohere_key = os.getenv('COHERE_API_KEY')
        if cohere_key:
            client = cohere.Client(api_key=cohere_key)
            response = client.generate(
                model='command',
                prompt='Test message',
                max_tokens=10
            )
            results['cohere'] = {'status': 'success', 'response': str(response.generations[0].text)[:50]}
        else:
            results['cohere'] = {'status': 'missing_key', 'response': 'No API key found'}
    except Exception as e:
        results['cohere'] = {'status': 'error', 'response': str(e)[:100]}
    
    # Test Groq
    try:
        from groq import Groq
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key:
            client = Groq(api_key=groq_key)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Test"}],
                model="llama3-8b-8192",
                max_tokens=10
            )
            results['groq'] = {'status': 'success', 'response': response.choices[0].message.content[:50]}
        else:
            results['groq'] = {'status': 'missing_key', 'response': 'No API key found'}
    except Exception as e:
        results['groq'] = {'status': 'error', 'response': str(e)[:100]}
    
    # Test Mistral
    try:
        from mistralai.client import MistralClient
        mistral_key = os.getenv('MISTRAL_API_KEY')
        if mistral_key:
            client = MistralClient(api_key=mistral_key)
            response = client.chat(
                model="mistral-tiny",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            results['mistral'] = {'status': 'success', 'response': response.choices[0].message.content[:50]}
        else:
            results['mistral'] = {'status': 'missing_key', 'response': 'No API key found'}
    except Exception as e:
        results['mistral'] = {'status': 'error', 'response': str(e)[:100]}
    
    # Test Together
    try:
        from together import Together
        together_key = os.getenv('TOGETHER_API_KEY')
        if together_key:
            client = Together(api_key=together_key)
            response = client.chat.completions.create(
                model="meta-llama/Llama-2-7b-chat-hf",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            results['together'] = {'status': 'success', 'response': response.choices[0].message.content[:50]}
        else:
            results['together'] = {'status': 'missing_key', 'response': 'No API key found'}
    except Exception as e:
        results['together'] = {'status': 'error', 'response': str(e)[:100]}
    
    # Test OpenRouter
    try:
        from openai import OpenAI
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        if openrouter_key:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_key
            )
            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct:free",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            results['openrouter'] = {'status': 'success', 'response': response.choices[0].message.content[:50]}
        else:
            results['openrouter'] = {'status': 'missing_key', 'response': 'No API key found'}
    except Exception as e:
        results['openrouter'] = {'status': 'error', 'response': str(e)[:100]}
    
    return results

if __name__ == "__main__":
    results = asyncio.run(test_all_apis())
    for provider, result in results.items():
        print(f"{provider}: {result}")
