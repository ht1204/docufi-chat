from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.8,
    api_key=OPENAI_API_KEY
)


def get_chat_response(user_input, doc_data):
    facts = doc_data.get('facts', {})
    if not facts:
        return "I couldn't find any specific financial data (Revenue, EBITDA, YoY growth) in the document you uploaded."

    fact_text = ". ".join([f"{k}: {v}" for k, v in facts.items()])
    prompt = f"User: {user_input}\n\nHere are some document facts: {fact_text}\nAnswer based on the above facts."

    messages = [HumanMessage(content=prompt)]
    response = llm(messages).content
    return response

