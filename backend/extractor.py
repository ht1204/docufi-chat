import json
import re
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from utils import load_pages_with_keywords

# Clean related keyword data.
def clean_fact(value):
    if not value or str(value).lower() == "null":
        return None
    return str(value).strip()

# Retrieve relevant important keywords info.
def extract_facts(filepath):
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    keywords = ["revenue", "Revenue", "EBITDA", "ebitda", "YoY", "YoY growth"]
    text = load_pages_with_keywords(filepath, keywords)
   
    if not text.strip():
        print("No relevant content found.")
        return {}

    prompt = (
        "You are a financial data extraction tool.\n\n"
        "Extract only the following values if they are explicitly stated in the document:\n"
        "- Revenue (e.g. '$1,945 million')\n"
        "- EBITDA (e.g. '$450M')\n"
        "- YoY growth (e.g. '3.2%')\n\n"
        "IMPORTANT FORMATTING RULES:\n"
        "1. Return ONLY valid JSON without any markdown code fences\n"
        "2. Do not include any text outside the JSON structure\n"
        "3. Use 'null' (unquoted) for missing values\n"
        "4. Never add explanations or comments\n\n"
        "Required output format:\n"
        "{\"Revenue\": \"...\", \"EBITDA\": \"...\", \"YoY growth\": \"...\"}\n\n"
        f"Document:\n{text}"
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0.15, api_key=OPENAI_API_KEY)
    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        # Remove markdown code fences if present
        json_str = re.sub(r'^```json|```$', '', response.content, flags=re.MULTILINE).strip()
        
        raw = json.loads(json_str)
        
        facts = {
            "Revenue": clean_fact(raw.get("Revenue")),
            "EBITDA": clean_fact(raw.get("EBITDA")),
            "YoY growth": clean_fact(raw.get("YoY growth"))
        }
        
        # Remove null values
        facts = {k: v for k, v in facts.items() if v is not None}
        
        print("Extracted facts:", facts)
        return facts
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed. Raw response: {response.content}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {}
    
