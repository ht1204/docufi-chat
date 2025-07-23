from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

# Parse uploaded document to text - first version
def load_and_embed(file):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(file)
    elif file.endswith(".docx"):
        loader = Docx2txtLoader(file)
    else:
        loader = TextLoader(file)
    return loader.load()[0].page_content

# Parse document to text and find related keywords info in doc pages to feed chatbot
def load_pages_with_keywords(filepath, keywords):
    loader = PyPDFLoader(filepath)
    pages = loader.load_and_split()

    relevant_pages = [
        page.page_content
        for page in pages
        if any(keyword.lower() in page.page_content.lower() for keyword in keywords)
    ]

    print(f"Found {len(relevant_pages)} relevant pages.")
    return "\n\n".join(relevant_pages)