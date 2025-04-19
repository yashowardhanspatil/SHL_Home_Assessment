# SHL_Home_Assessment
This repository consists of all the files that have been utilized to build the SHL Home Assessment (GEN AI, RAG based SHL Assessment Recommendation System) project. 

#  SHL Assessment Recommendation Engine

This project is part of a take-home research intern assignment for SHL. It uses Google Gemini Pro and Retrieval-Augmented Generation (RAG) to recommend relevant SHL assessments based on job descriptions or recruiter queries.

---

## 🌐 Live Demos

- 🔎 **Streamlit UI**: [Try the Web App](https://test-recommender-ai.streamlit.app/)
- 🧠 **API Endpoint**: [FastAPI on Render](https://shl-api-ifyj.onrender.com/recommend)

---

## 🚀 Features

- Accepts either a **text query** or a **URL to a job description**
- Uses **Gemini Pro** to refine and extract the intent of the job
- Embeds both queries and product catalog using **Gemini Embedding API**
- Performs **semantic vector search** with **FAISS**
- Displays **top 10 recommended assessments** with attributes:
  - Assessment Title
  - Duration
  - Test Type
  - Remote/Adaptive support
  - Description

---

## ⚙️ Tech Stack

| Layer         | Technology                         |
|---------------|-------------------------------------|
| LLM           | Gemini Pro (Gemini 1.5 / Gemini Pro Embedding) |
| Embedding DB  | FAISS                              |
| Backend       | FastAPI (deployed on Render)       |
| Frontend      | Streamlit (deployed on Streamlit Cloud) |
| Preprocessing | BeautifulSoup, Requests            |

---

## 📂 Endpoints

### `GET /health`
Returns simple health check:

```json
{"status": "ok"}
```

---

### `POST /recommend`

**Example Request:**
```json
{
  "query": "Looking for a Python + SQL developer test under 45 minutes"
}
```
**OR**
```json
{
  "url": "https://example.com/job-description"
}
```

**Example Response:**
```json
{
  "recommendations": [
    {
      "title": "CodeAbility – Python & SQL",
      "url": "https://www.shl.com/product/codeability-python",
      "assessment_length_minutes": 40,
      "remote_testing": "Yes",
      "adaptive": "No",
      "test_type": ["Ability & Aptitude", "Technical"],
      "description": "This assessment measures real-world coding skills..."
    }
  ]
}
```

---

## 🧠 Gemini Query Prompt

```text
Given this job description, extract the key skills, roles, and test preferences.
Return a short search query to find matching assessments.
```

---

## 🗂️ Project Structure

```
.
├── app.py                # Streamlit frontend
├── api.py                # FastAPI backend
├── embedder.py           # Gemini embedding logic
├── retriever.py          # FAISS vector search
├── utils.py              # JD scraping & query refinement (Gemini)
├── generate_index.py     # Build FAISS index from catalog
├── shl_products_cleaned.json          # SHL product catalog (pre-scraped)
├── faiss_index.index     # FAISS binary index
├── faiss_metadata.pkl    # Catalog metadata
├── requirements.txt
├── seltest1.py          # Web Scraping tool using Selenium, Bs4
└── .gitignore
```

---

## 🧪 Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Generate FAISS index (only once)
python generate_index.py

# Run Streamlit frontend
streamlit run app.py

# Run FastAPI backend
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## 📁 .gitignore Example

```gitignore
.env
venv/
web_scrap/
__pycache__/
*.pyc

```

---

## 🧑‍💼 Author

This project was developed as part of a Generative AI internship assignment for SHL.
```


