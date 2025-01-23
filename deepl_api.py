from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api.deepl.com/v2"

async def deepl_request(
    endpoint: str,
    data: dict,
    method: str = "POST",
    files: dict = None
):
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}
    async with httpx.AsyncClient() as client:
        try:
            if method == "POST":
                response = await client.post(
                    f"{DEEPL_API_URL}/{endpoint}",
                    headers=headers,
                    data=data,
                    files=files
                )
            elif method == "GET":
                response = await client.get(
                    f"{DEEPL_API_URL}/{endpoint}",
                    headers=headers,
                    params=data
                )
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def get_error_detail(response: httpx.Response) -> str:
    try:
        error_data = response.json()
        return error_data.get("message", response.text)
    except json.JSONDecodeError:
        return response.text

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.post("/translate_text")
async def translate_text(
    text: str = Form(...),
    target_lang: str = Form(...),
    source_lang: str = Form(None)
):
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
        detail = get_error_detail(response)
        raise HTTPException(status_code=response.status_code, detail=detail)

@app.post("/translate_document")
async def translate_document(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    source_lang: str = Form(None)
):
    if source_lang and source_lang == target_lang:
        raise HTTPException(
            status_code=400,
            detail="Source and target languages must be different"
        )

    allowed_extensions = ['.txt', '.pdf', '.docx', '.pptx', '.xlsx']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    data = {"target_lang": target_lang}
    if source_lang:
        data["source_lang"] = source_lang

    files = {"file": (file.filename, file.file, file.content_type)}
    response = await deepl_request("document", data, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        detail = get_error_detail(response)
        raise HTTPException(status_code=response.status_code, detail=detail)

@app.get("/document_status/{document_id}")
async def document_status(document_id: str, document_key: str):
    response = await deepl_request(
        f"document/{document_id}",
        {"document_key": document_key},
        method="GET"
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        detail = get_error_detail(response)
        raise HTTPException(status_code=response.status_code, detail=detail)

@app.get("/download_document/{document_id}")
async def download_document(document_id: str, document_key: str):
    response = await deepl_request(
        f"document/{document_id}/result",
        {"document_key": document_key},
        method="GET"
    )
    
    if response.status_code == 200:
        # Get the content type from DeepL's response
        content_type = response.headers.get("content-type", "application/octet-stream")
        
        # Enhanced MIME type mapping with more specific types
        file_extensions = {
            "application/pdf": ".pdf",
            "text/plain": ".txt",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/json": ".json",  # Add JSON handling
            "application/octet-stream": ".bin"  # Default binary
        }
        
        # Get extension based on content type, fallback to .bin
        extension = file_extensions.get(content_type, ".bin")
        
        # Create temporary file with proper extension
        temp_file = f"translated_{document_id}{extension}"
        
        # Write binary content
        with open(temp_file, "wb") as f:
            f.write(response.content)
        
        # Return file with proper headers
        return FileResponse(
            path=temp_file,
            media_type=content_type,
            filename=f"translated_document{extension}",
            headers={
                "Content-Disposition": f"attachment; filename=translated_document{extension}"
            }
        )
    else:
        detail = get_error_detail(response)
        raise HTTPException(status_code=response.status_code, detail=detail)