import faiss
import pickle
import numpy as np
from embedder import get_embedding

def load_index():
    index = faiss.read_index("faiss_index.index")
    with open("faiss_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def search(query: str, k=10):
    index, metadata = load_index()
    query_vec = np.array([get_embedding(query, task_type="retrieval_query")]).astype("float32")
    _, I = index.search(query_vec, k)
    return [metadata[i] for i in I[0]]
