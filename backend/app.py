from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import get_chat_response
from extractor import extract_facts
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

doc_store = {}  

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    doc_id = str(uuid.uuid4())
    extension = os.path.splitext(file.filename)[1]
    filename = f"{doc_id}{extension}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)


    facts = extract_facts(filepath)
    
    ## Logger: extract financial facts
    print("Extracted facts:", facts) 
    
    doc_store[doc_id] = {
        'facts': facts,
        'filepath': filepath
    }

    return jsonify({ 'docId': doc_id }), 200


@app.route('/conversation', methods=['POST'])
def conversation():
    data = request.get_json()
    doc_id = data.get("docId")
    message = data.get("message")

    doc_content = doc_store.get(doc_id, "")
    facts = {}
    
    MAX_CHARS = 24000
    
    if len(doc_content) > MAX_CHARS:
        doc_content = doc_content[:MAX_CHARS] 

    response = get_chat_response(message, doc_content)
    return jsonify({"reply": response})



@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({ 'reply': 'Hello World!' })



if __name__ == '__main__':
    app.run(debug=True)
