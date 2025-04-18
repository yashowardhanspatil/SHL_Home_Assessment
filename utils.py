import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_url(url: str) -> str:
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip()
    except Exception as e:
        return f"Error fetching URL: {e}"

def refine_query_with_gemini(raw_text: str) -> str:
    prompt = f"""
    Given this job description, extract the key skills, roles, and test preferences. 
    Return a short search query to find matching assessments.

    Job Description:
    \"\"\"
    {raw_text}
    \"\"\"
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()
