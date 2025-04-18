from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import search
from utils import extract_text_from_url, refine_query_with_gemini

app = FastAPI()

class QueryRequest(BaseModel):
    query:str = None
    url:str = None

@app.get("/health")
def health_check():
    return {"status":"healthy"}

@app.post("/recommend")
def recommend(data: QueryRequest):
    if not data.query and not data.url:
        raise HTTPException(status_code=400, detail="Please provide either a query or a URL.")
    
    try:
        raw_text = extract_text_from_url(data.url) if data.url else data.query
        refined_query = refine_query_with_gemini(raw_text)
        results = search(refined_query)

        return {"recommended_assessments": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))