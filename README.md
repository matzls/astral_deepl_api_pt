# DeepL Translation API Interface

This project provides a web-based interface for the DeepL Translation API, allowing users to translate text and documents using DeepL's powerful translation service.

## Features

- Text translation with support for multiple languages
- Document translation (supports .txt, .pdf, .docx, .pptx, .xlsx)
- Auto-detection of source language
- Translation history for text translations
- Character count for text input
- Error handling and user feedback

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- httpx
- python-dotenv
- A DeepL API key

## Installation

1. Clone this repository:   ```
   git clone <repository-url>
   cd <repository-directory>   ```

2. Install the required packages:   ```
   pip install fastapi uvicorn httpx python-dotenv   ```

3. Create a `.env` file in the project root and add your DeepL API key:   ```
   DEEPL_API_KEY=your_api_key_here   ```

## Usage

1. Start the FastAPI server:   ```
   uvicorn ASTRAL.Code.Morla.Deepl\ UI.deepl_api:app --reload   ```
   Make sure you're in the correct directory (likely the GitHub directory) when running this command,
   and that your virtual environment (if you're using one) is activated.

2. Open a web browser and navigate to `http://127.0.0.1:8000`

3. Use the interface to translate text or documents:
   - For text translation, enter the text, select source and target languages, and click "Translate Text"
   - For document translation, upload a file, select source and target languages, and click "Translate Document"

## Project Structure

- `deepl_api.py`: FastAPI backend that handles API requests and communicates with the DeepL API
- `index.html`: Frontend interface for text and document translation
- `README.md`: This file, containing project information and instructions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]

## Acknowledgements

- [DeepL](https://www.deepl.com) for providing the translation API
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Axios](https://axios-http.com/) for HTTP requests in the frontend
