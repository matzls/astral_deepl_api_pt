import httpx
import os
from typing import Optional, Dict, Any, List
import json
from dotenv import load_dotenv
from deepl_api import DEEPL_API_URL

# Load environment variables from .env
load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

print(f"API Key present: {'Yes' if DEEPL_API_KEY else 'No'}")
print(f"Using API URL: {DEEPL_API_URL}")

async def improve_text(
    texts: List[str],
    language: Optional[str] = None,
    context: Optional[str] = None,
    # style: Optional[str] = None,    # Example for future usage if DeepL adds "style"
    # domain: Optional[str] = None,   # Example for future usage if DeepL adds "domain"
) -> Dict[Any, Any]:
    """
    Improve text using DeepL Write API.

    Args:
        texts: A list of strings to rephrase/improve.
        language: Two-letter or five-letter language code (e.g. "EN" or "EN-US").
        context: Optional context for improvement (e.g. "Email to a business colleague").
        style: Placeholder for future usage if DeepL adds a 'style' parameter.
        domain: Placeholder for future usage if DeepL adds domain-specific improvements.
    """
    url = f"{DEEPL_API_URL}/v2/write/rephrase"
    
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Build the request payload
    data = {
        "text": texts,  # list of strings
        "language": language if language else "EN-US",
    }
    if context:
        data["context"] = context
    
    # Uncomment if the API offers these fields in the future
    # if style:
    #     data["style"] = style
    # if domain:
    #     data["domain"] = domain

    print(f"\nMaking request to: {url}")
    print(f"Request data:\n{json.dumps(data, indent=2)}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Full error response:\n{e.response.text if hasattr(e, 'response') else str(e)}")
            return {"error": str(e)}

async def run_tests():
    """
    Runs multiple test scenarios against the DeepL Write API for broader coverage.
    """
    test_scenarios = [
        {
            "description": "Single short sentence, default language",
            "texts": ["I am very happy for meet you yesterday."],
            "language": None,
            "context": None
        },
        {
            "description": "Single short sentence, with context and explicit language",
            "texts": ["I am very happy for meet you yesterday."],
            "language": "EN-US",
            "context": "Email to a business colleague"
        },
        {
            "description": "Multiple lines of text",
            "texts": [
                "I love programming in Python.",
                "Writing great code is essential to building robust applications."
            ],
            "language": "EN-US"
        },
        {
            "description": "Multiple lines, with context",
            "texts": [
                "Your resume is quite impressive.",
                "We would appreciate your feedback as soon as possible."
            ],
            "language": "EN-US",
            "context": "Email HR message"
        },
        # If DeepL adds style/domain parameters, you can add more tests here
        # {
        #     "description": "Experiment with hypothetical 'style' parameter",
        #     "texts": ["Hello", "This is a second text."],
        #     "language": "EN-US",
        #     "style": "friendly"
        # }
    ]

    for i, scenario in enumerate(test_scenarios, start=1):
        print(f"\n--- Test {i}: {scenario['description']} ---")
        result = await improve_text(
            texts=scenario["texts"],
            language=scenario.get("language"),
            context=scenario.get("context")
            # style=scenario.get("style"),
            # domain=scenario.get("domain")
        )
        print("Result:\n", json.dumps(result, indent=2))
        print("-----------------------------------------------------------")

async def main():
    await run_tests()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())