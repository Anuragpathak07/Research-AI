# storage/vector_store.py
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, meta):
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata.extend(meta)

    def search(self, query_embedding, k=5):
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )
        return [self.metadata[i] for i in indices[0]]
