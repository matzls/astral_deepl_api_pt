import streamlit as st
import httpx
import json
import os
import time

st.set_page_config(
    page_title="DeepL API Testing Interface",
    layout="wide"
)

def main():
    st.title("DeepL API Testing Interface")
    
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
                        target_lang = "DE"  # Default to German for testing
                        data = {
                            "text": source_text,
                            "target_lang": target_lang
                        }
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
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with tab2:
        st.header("Document Translation")
        
        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["txt", "pdf", "docx", "pptx", "xlsx"]
        )
        
        target_lang = st.selectbox(
            "Target Language",
            ["DE", "EN", "FR", "ES"],
            key="doc_target_lang"
        )
        
        if uploaded_file and st.button("Translate Document"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                data = {"target_lang": target_lang}
                
                with st.spinner("Uploading document..."):
                    response = httpx.post(
                        "http://127.0.0.1:8000/translate_document",
                        files=files,
                        data=data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        doc_id = result["document_id"]
                        doc_key = result["document_key"]
                        
                        progress_placeholder = st.empty()
                        status_container = st.empty()
                        
                        # Poll for status
                        while True:
                            try:
                                status_response = httpx.get(
                                    f"http://127.0.0.1:8000/document_status/{doc_id}",
                                    params={"document_key": doc_key},
                                    timeout=100
                                )
                                
                                if status_response.status_code == 200:
                                    status = status_response.json()
                                    status_container.write(f"Current status: {status['status'].capitalize()}")
                                    
                                    if status["status"] == "done":
                                        progress_placeholder.success("Translation complete!")
                                        download_url = f"http://127.0.0.1:8000/download_document/{doc_id}?document_key={doc_key}"
                                        st.markdown(
                                            f'<a href="{download_url}" target="_blank" style="padding: 0.5rem 1rem; background-color: #4CAF50; color: white; border-radius: 0.25rem; text-decoration: none;">Download Translated Document</a>',
                                            unsafe_allow_html=True
                                        )
                                        break
                                    elif status["status"] == "error":
                                        progress_placeholder.error("Translation failed!")
                                        break
                                    
                                    time.sleep(2)
                                else:
                                    st.error("Error checking translation status")
                                    break
                                    
                            except httpx.TimeoutException:
                                st.error("Status check timed out")
                                break
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                                break
                    else:
                        st.error("Failed to initiate translation")
                        
            except Exception as e:
                st.error(f"Error during document translation: {str(e)}")

    with tab3:
        st.header("DeepL Write")
        st.info("DeepL Write feature coming soon...")

if __name__ == "__main__":
    main()