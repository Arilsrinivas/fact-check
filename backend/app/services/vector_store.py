from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        # Lightweight model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.claims_map = {} # Map Index ID -> Claim ID

    def add_claim(self, claim_id: int, text: str):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding).astype('float32'))
        
        # Store verification key
        idx = self.index.ntotal - 1
        self.claims_map[idx] = claim_id
        return str(idx)

    def find_similar(self, text: str, k=1):
        embedding = self.model.encode([text])
        D, I = self.index.search(np.array(embedding).astype('float32'), k)
        
        results = []
        if I[0][0] != -1:
            # Found potential match
            idx = I[0][0]
            distance = D[0][0]
            if idx in self.claims_map and distance < 0.5: # Threshold
                results.append(self.claims_map[idx])
        
        return results

vector_store = VectorStore()
