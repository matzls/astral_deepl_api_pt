from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

app = FastAPI()
"""
cd /Users/mg/Desktop/GitHub/Astral_Code/astral_deepl_api_pt
uvicorn deepl_api:app --reload
"""

# Mount the static files directory
app.mount("/static", StaticFiles(directory="."), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api.deepl.com/v2"

async def deepl_request(endpoint, data, files=None):
    """
    Make a request to the DeepL API.

    Args:
    endpoint (str): The API endpoint to call.
    data (dict): The data to send with the request.
    files (dict, optional): Files to upload for document translation.

    Returns:
    httpx.Response: The response from the DeepL API.
    """
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DEEPL_API_URL}/{endpoint}", headers=headers, data=data, files=files)
    return response

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.post("/translate_text")
async def translate_text(text: str = Form(...), target_lang: str = Form(...), source_lang: str = Form(None)):
    """
    Translate text using the DeepL API.

    Args:
    text (str): The text to translate.
    target_lang (str): The target language code.
    source_lang (str, optional): The source language code. If not provided, DeepL will auto-detect the language.

    Returns:
    dict: A dictionary containing the translated text.
    """
    print(f"Received text: {text}")
    print(f"Target language: {target_lang}")
    print(f"Source language: {source_lang}")
    
    data = {
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        data["source_lang"] = source_lang

    response = await deepl_request("translate", data)
    
    if response.status_code == 200:
        result = response.json()
        return {"translated_text": result["translations"][0]["text"]}
    else:
        print(f"DeepL API error: {response.status_code} - {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/translate_document")
async def translate_document(file: UploadFile = File(...), target_lang: str = Form(...), source_lang: str = Form(None)):
    """
    Translate a document using the DeepL API.

    Args:
    file (UploadFile): The document file to translate.
    target_lang (str): The target language code.
    source_lang (str, optional): The source language code. If not provided, DeepL will auto-detect the language.

    Returns:
    dict: A dictionary containing the document_id and document_key for status checking and download.
    """
    print(f"Received document: {file.filename}")
    print(f"Target language: {target_lang}")
    print(f"Source language: {source_lang}")
    
    allowed_extensions = ['.txt', '.pdf', '.docx', '.pptx', '.xlsx']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    data = {
        "target_lang": target_lang,
    }
    if source_lang:
        data["source_lang"] = source_lang

    files = {"file": (file.filename, file.file, file.content_type)}
    
    response = await deepl_request("document", data, files)
    
    print(f"DeepL API response status: {response.status_code}")
    print(f"DeepL API response content: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        return {"document_id": result["document_id"], "document_key": result["document_key"]}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/document_status/{document_id}")
async def document_status(document_id: str, document_key: str):
    print(f"Checking status for document_id: {document_id}")
    data = {"document_key": document_key}
    response = await deepl_request(f"document/{document_id}", data)
    
    print(f"DeepL API status response: {response.status_code}")
    print(f"DeepL API status content: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/download_document/{document_id}")
async def download_document(document_id: str, document_key: str):
    data = {"document_key": document_key}
    response = await deepl_request(f"document/{document_id}/result", data)
    
    if response.status_code == 200:
        temp_file = f"temp_{uuid.uuid4()}.pdf"
        with open(temp_file, "wb") as f:
            f.write(response.content)
        return FileResponse(temp_file, filename="translated_document.pdf", media_type="application/pdf")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)