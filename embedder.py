import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str, task_type="retrieval_document") -> list:
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type=task_type
    )
    return response['embedding']
