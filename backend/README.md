## Backend – Docufi Mini-Chat (Flask + LangChain)

This backend service enables users to:

- Upload PDF files
- Extract **verbatim** financial facts: **Revenue**, **EBITDA**, and **YoY growth**
- Chat about the document using a language model (GPT-4o) with injected facts

## 🛠 Requirements

- Python 3.13
- `virtualenv` or `venv`
- Add Personal OpenAI API key

## Setup
### 1. Go to backend
cd backend

### 2. Create and activate virtual environment
python -m venv .venv
source venv/bin/activate

For windows OS: `.venv\Scripts\activate`

### 3. Install dependencies
`pip install -r requirements.txt`

If previous command does not work, try this command:
`pip install Flask flask-cors python-dotenv langchain langchain-openai langchain-community openai pypdf python-docx docx2txt tiktoken pydantic
`

### 4. Add your OpenAI key
Create a `.env` file and add the `OPENAI_API_KEY`

# 5. Run the Flask server
`flask run`

## API Endpoints
1. POST /upload
Upload a file and extract key financial facts.

- Request:

Content-Type: multipart/form-data
Payload: file (PDF)

- Response:

```json{ "docId": "<uuid>" }```


2. POST /conversation
Send a message tied to a document and get a smart reply using extracted facts.

Request:
```json
{
  "docId": "<uuid>",
  "message": "What is the reported revenue?"
}
```

Response:
```json
{
  "reply": "Revenue was $1,945 million as reported in FY-24."
}
```
3. GET /healthcheck
Simple service backend server check.

Response:
```json
{ "reply": "Hello World!" }
```
 
### How It Works
extractor.py: Uses LangChain and GPT-4o to extract only explicitly written values.

utils.py: Scans documents and sends only relevant pages (with keywords) to the LLM.

chat.py: Embeds the extracted facts into the LLM prompt to answer based on the uploaded content.

