import streamlit as st
import httpx
import json

st.set_page_config(
    page_title="DeepL API Testing Interface",
    layout="wide"
)

def main():
    st.title("DeepL API Testing Interface")
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs(["Translate Text", "Translate Files", "DeepL Write"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox(
                "Detect language",
                ["Auto Detect", "English", "German", "French", "Spanish"],
                index=0
            )
            
            source_text = st.text_area(
                "Type to translate",
                height=200,
                placeholder="Enter text here..."
            )
            
            if st.button("Translate"):
                if source_text:
                    try:
                        # Convert display language to API code
                        target_lang = "DE"  # For testing, we'll use German as default
                        
                        # Prepare the request
                        data = {
                            "text": source_text,
                            "target_lang": target_lang
                        }
                        
                        # Make request to your FastAPI endpoint
                        response = httpx.post(
                            "http://127.0.0.1:8000/translate_text",
                            data=data
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            with col2:
                                st.text_area(
                                    "Translation",
                                    value=result["translated_text"],
                                    height=200
                                )
                        else:
                            st.error(f"Translation failed: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please enter some text to translate")
        
        with col2:
            st.selectbox(
                "Target language",
                ["English", "German", "French", "Spanish"],
                index=1
            )
            st.text_area(
                "Translation",
                height=200,
                disabled=True
            )

    with tab2:
        st.header("Document Translation")
        uploaded_file = st.file_uploader(
            "Upload a document (PDF, DOCX, PPTX)",
            type=["pdf", "docx", "pptx"]
        )
        if uploaded_file:
            st.info("Document upload feature coming soon...")

    with tab3:
        st.header("DeepL Write")
        st.info("DeepL Write feature coming soon...")

if __name__ == "__main__":
    main()