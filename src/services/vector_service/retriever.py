import numpy as np

class Retriever:
    def __init__(self, vector_store, embedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def get_relevant_chunks(self, query, top_k=10):
        query_vector = self.embedder.generate_embeddings([query])
        # FAISS search
        distances, indices = self.vector_store.index.search(
            np.array(query_vector).astype('float32'), top_k
        )

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.vector_store.metadata):
                results.append({
                    "doc": self.vector_store.metadata[idx], 
                    "score": float(distances[0][i])
                })
        return results