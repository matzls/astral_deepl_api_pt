import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables (ensure your .env includes DEEPL_API_KEY)
load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api.deepl.com"

def improve_text_sync(text_list, language="EN-US", context=None):
    """
    Synchronous version of the improve_text function that calls the DeepL Write /v2/write/rephrase endpoint.
    text_list: list of strings
    language: e.g. "EN-US", "DE", etc.
    context: optional context string
    """
    url = f"{DEEPL_API_URL}/v2/write/rephrase"
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": text_list,   # array of strings
        "language": language
    }
    if context:
        payload["context"] = context
    
    # Make the POST request
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    st.title("DeepL Write Demo")
    st.write("Enter one or more lines to improve with the DeepL Write API.")
    
    # User inputs
    user_text = st.text_area("Enter your text (multiple lines optional)", 
                             value="I am very happy for meet you yesterday.")
    language = st.text_input("Target language code (e.g. EN-US, DE)", value="EN-US")
    context = st.text_input("Context (optional)", value="Email to a business colleague")

    if st.button("Improve Text"):
        # Split user_text by lines to create a list
        lines = [line.strip() for line in user_text.split("\n") if line.strip()]
        
        try:
            rephrased_data = improve_text_sync(lines, language=language, context=context)
            
            st.subheader("DeepL Write Response")
            st.json(rephrased_data)

            improvements = rephrased_data.get("improvements", [])
            if improvements:
                st.subheader("Improved Lines")
                for i, imp in enumerate(improvements, start=1):
                    st.write(f"Line {i}: {imp.get('text')}")
            else:
                st.write("No improvements found in response.")

        except requests.HTTPError as e:
            st.error(f"Error calling DeepL Write API: {str(e)}")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()