import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

documents = [
    "La inteligencia artificial es un campo fascinante.",
    "El aprendizaje automático es un subcampo de la IA.",
    "Los vehículos eléctricos están transformando el transporte."
]

model = SentenceTransformer('all-MiniLM-L6-v2')
document_embeddings = model.encode(documents)

dimension = document_embeddings.shape[1]  # corregido: solo la dimensión del vector
index = faiss.IndexFlatL2(dimension)
index.add(document_embeddings.astype('float32'))

query = "¿Qué es el aprendizaje automático?"
query_embedding = model.encode([query]).astype('float32')
distances, indices = index.search(query_embedding, k=1)

retrieved_doc = documents[indices[0][0]]  # acceder al índice correcto
print(f"Documento recuperado: {retrieved_doc}")
