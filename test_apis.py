#!/usr/bin/env python3

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_cohere_api():
    """Test Cohere API connectivity"""
    try:
        import cohere
        co = cohere.Client(os.getenv('COHERE_API_KEY'))
        response = co.generate(
            model='command',
            prompt='Hello, this is a test. Respond with just "Cohere API working"',
            max_tokens=10
        )
        return f"✅ Cohere: {response.generations[0].text.strip()}"
    except Exception as e:
        return f"❌ Cohere: {str(e)[:100]}"

async def test_groq_api():
    """Test Groq API connectivity"""
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Say 'Groq API working'"}],
            model="llama3-8b-8192",
            max_tokens=10
        )
        return f"✅ Groq: {response.choices[0].message.content.strip()}"
    except Exception as e:
        return f"❌ Groq: {str(e)[:100]}"

async def test_mistral_api():
    """Test Mistral API connectivity"""
    try:
        from mistralai.client import MistralClient
        from mistralai.models.chat_completion import ChatMessage
        
        client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))
        response = client.chat(
            model="mistral-tiny",
            messages=[ChatMessage(role="user", content="Say 'Mistral API working'")],
            max_tokens=10
        )
        return f"✅ Mistral: {response.choices[0].message.content.strip()}"
    except Exception as e:
        return f"❌ Mistral: {str(e)[:100]}"

async def test_together_api():
    """Test Together API connectivity"""
    try:
        import together
        together.api_key = os.getenv('TOGETHER_API_KEY')
        
        response = together.Complete.create(
            prompt="Say 'Together API working'",
            model="togethercomputer/RedPajama-INCITE-Base-3B-v1",
            max_tokens=10
        )
        return f"✅ Together: {response['output']['choices'][0]['text'].strip()}"
    except Exception as e:
        return f"❌ Together: {str(e)[:100]}"

async def main():
    print("🔍 Testing API connectivity...")
    print("-" * 50)
    
    # Test all APIs concurrently
    results = await asyncio.gather(
        test_cohere_api(),
        test_groq_api(),
        test_mistral_api(),
        test_together_api(),
        return_exceptions=True
    )
    
    for result in results:
        print(result)
    
    print("-" * 50)
    print("API test complete")

if __name__ == "__main__":
    asyncio.run(main())
