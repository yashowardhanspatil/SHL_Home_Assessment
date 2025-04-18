import json
import faiss
import numpy as np
import pickle
from embedder import get_embedding

with open("shl_products_cleaned.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
metadata = []

for entry in data:
    combined = f"""
    Title: {entry['title']}
    Test Types: {', '.join(entry['test_type'])}
    Remote Testing: {entry['remote_testing']}
    Adaptive: {entry['adaptive']}
    Duration: {entry['assessment_length_minutes']} minutes
    Description: {entry['description']}
    """

    texts.append(combined)
    metadata.append(entry)

vectors = np.array([get_embedding(text) for text in texts]).astype("float32")

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

faiss.write_index(index, "faiss_index.index")
with open("faiss_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("FAISS index built and saved using Gemini embeddings.")
