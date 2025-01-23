import httpx
import os
from typing import Optional, Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api.deepl.com"  # Base URL for DeepL API

print(f"API Key present: {'Yes' if DEEPL_API_KEY else 'No'}")
print(f"Using API URL: {DEEPL_API_URL}")

async def improve_text(
    text: str,
    context: Optional[str] = None,
    language: Optional[str] = None
) -> Dict[Any, Any]:
    """
    Improve text using DeepL Write API
    """
    url = f"{DEEPL_API_URL}/v2/write"
    
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "text": text,
    }
    
    # Add optional parameters if provided
    if context:
        data["context"] = context
    if language:
        data["language"] = language

    print(f"Making request to: {url}")
    print(f"With data: {json.dumps(data, indent=2)}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            print(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Full error response: {e.response.text if hasattr(e, 'response') else str(e)}")
            return {"error": str(e)}

async def main():
    # Test cases
    text_to_improve = "I am very happy for meet you yesterday."
    context = "Email to a business colleague"
    
    # Test 1: Basic improvement
    print("\nTest 1: Basic text improvement")
    result = await improve_text(text_to_improve)
    print(json.dumps(result, indent=2))
    
    # Test 2: With context and language
    print("\nTest 2: Text improvement with context and language")
    result = await improve_text(text_to_improve, context=context, language="EN-US")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())