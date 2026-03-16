import faiss
import os
import numpy as np
import pickle
import json
from pathlib import Path
from config.settings import VECTOR_DB_PATH

class VectorStore:
    def __init__(self, dimension):
        self.dimension = dimension
        faiss.omp_set_num_threads(os.cpu_count())
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata = []
        self.file_structure = [] # Physical file map

    def add_to_index(self, embeddings, chunks):
        vectors = np.array(embeddings).astype('float32')
        self.index.add(vectors)
        self.metadata.extend(chunks)