import httpx
import os
from typing import Optional, Dict, Any, List
import json
from dotenv import load_dotenv
from deepl_api import DEEPL_API_URL

# Load environment variables
load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

print(f"API Key present: {'Yes' if DEEPL_API_KEY else 'No'}")
print(f"Using API URL: {DEEPL_API_URL}")

async def improve_text(
    texts: List[str],
    target_lang: str,
    writing_style: Optional[str] = None,
    tone: Optional[str] = None
) -> Dict[Any, Any]:
    """
    Improve text using DeepL Write API.
    """
    url = f"{DEEPL_API_URL}/v2/write/rephrase"
    
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "text": texts,
        "target_lang": target_lang
    }
    
    if writing_style:
        data["writing_style"] = writing_style
    elif tone:
        data["tone"] = tone

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
    Tests comparing array structures and parameters
    """
    # Base paragraph as one string
    full_paragraph = (
        "The research findings indicate significant progress in renewable energy adoption. "
        "Solar and wind installations have doubled in the past year. "
        "Energy storage solutions are becoming more cost-effective. "
        "These developments suggest a promising future for sustainable power generation."
    )
    
    # Same paragraph split into sentences
    split_sentences = [
        "The research findings indicate significant progress in renewable energy adoption.",
        "Solar and wind installations have doubled in the past year.",
        "Energy storage solutions are becoming more cost-effective.",
        "These developments suggest a promising future for sustainable power generation."
    ]

    test_scenarios = [
        {
            "description": "1a) Single array element - base test",
            "texts": [full_paragraph],
            "target_lang": "en-US"
        },
        {
            "description": "1b) Multiple array elements - base test",
            "texts": split_sentences,
            "target_lang": "en-US"
        },
        {
            "description": "2a) Single array + academic style",
            "texts": [full_paragraph],
            "target_lang": "en-US",
            "writing_style": "academic"
        },
        {
            "description": "2b) Multiple array + academic style",
            "texts": split_sentences,
            "target_lang": "en-US",
            "writing_style": "academic"
        },
        {
            "description": "3a) Single array + casual style",
            "texts": [full_paragraph],
            "target_lang": "en-US",
            "writing_style": "casual"
        },
        {
            "description": "3b) Multiple array + casual style",
            "texts": split_sentences,
            "target_lang": "en-US",
            "writing_style": "casual"
        },
        {
            "description": "4a) Single array + enthusiastic tone",
            "texts": [full_paragraph],
            "target_lang": "en-US",
            "tone": "enthusiastic"
        },
        {
            "description": "4b) Multiple array + enthusiastic tone",
            "texts": split_sentences,
            "target_lang": "en-US",
            "tone": "enthusiastic"
        },
        {
            "description": "5a) Single array + diplomatic tone",
            "texts": [full_paragraph],
            "target_lang": "en-US",
            "tone": "diplomatic"
        },
        {
            "description": "5b) Multiple array + diplomatic tone",
            "texts": split_sentences,
            "target_lang": "en-US",
            "tone": "diplomatic"
        }
    ]

    for i, scenario in enumerate(test_scenarios, start=1):
        print(f"\n=== Test {i}: {scenario['description']} ===")
        result = await improve_text(
            texts=scenario["texts"],
            target_lang=scenario["target_lang"],
            writing_style=scenario.get("writing_style"),
            tone=scenario.get("tone")
        )
        print("Result:\n", json.dumps(result, indent=2))
        print("=" * 80)

async def main():
    await run_tests()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())