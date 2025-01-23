import os
import httpx
from dotenv import load_dotenv
import asyncio
from typing import Dict, List

load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api.deepl.com/v2"

async def get_languages(type: str) -> List[Dict]:
    """Fetch languages from DeepL API for specified type (source/target)"""
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DEEPL_API_URL}/languages",
            headers=headers,
            params={"type": type}
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching {type} languages: {response.status_code}")
            return []

async def main():
    # Get both source and target languages
    source_langs = await get_languages("source")
    target_langs = await get_languages("target")
    
    print("\nSource Languages:")
    print("-----------------")
    for lang in source_langs:
        print(f"{lang['language']}: {lang['name']}")
    
    print("\nTarget Languages:")
    print("-----------------")
    for lang in target_langs:
        print(f"{lang['language']}: {lang['name']}")
    
    # Compare differences
    source_codes = {lang['language'] for lang in source_langs}
    target_codes = {lang['language'] for lang in target_langs}
    
    print("\nLanguages only available as source:")
    print("----------------------------------")
    print(source_codes - target_codes)
    
    print("\nLanguages only available as target:")
    print("----------------------------------")
    print(target_codes - source_codes)

if __name__ == "__main__":
    asyncio.run(main())
