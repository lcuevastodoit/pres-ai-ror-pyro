# Instalar librerías necesarias
# pip install langchain faiss-cpu sentence-transformers ollama llama-cpp-python pypdf
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM # O LlamaCpp para mayor control
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import os

# 1. Cargar y Chunkear Documentos
# Para este ejemplo, se usa un texto simple. En una aplicación real, se cargarían PDFs, etc.
text_content = """
La inteligencia artificial (IA) es un campo de la informática que se centra en la creación de máquinas inteligentes que pueden realizar tareas que normalmente requieren inteligencia humana. Esto incluye el aprendizaje, la resolución de problemas, el reconocimiento de patrones y la comprensión del lenguaje natural.
El aprendizaje automático (ML) es un subcampo de la IA que permite a los sistemas aprender de los datos sin ser programados explícitamente. Se basa en algoritmos que construyen un modelo a partir de datos de entrada para hacer predicciones o tomar decisiones.
Retrieval-Augmented Generation (RAG) es una técnica de IA que combina la recuperación de información con la generación de texto. Un sistema RAG primero busca información relevante en una base de datos (retriever) y luego utiliza esa información para generar una respuesta más precisa y contextualizada (generator).
FAISS (Facebook AI Similarity Search) es una biblioteca para la búsqueda eficiente de similitud de vectores, muy utilizada en sistemas RAG como base de datos de vectores local.
Ollama es una plataforma que permite ejecutar grandes modelos de lenguaje (LLMs) localmente en tu máquina, simplificando su gestión y uso.
"""
# LangChain requiere que los documentos sean de tipo Document
from langchain_core.documents import Document
documents =  [Document(page_content=text_content)]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# 2. Generar Embeddings y Crear Base de Vectores FAISS
# Usar un modelo de embeddings optimizado para CPU
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.from_documents(chunks, embedding_model)

# 3. Inicializar el LLM Local (usando Ollama como ejemplo)
# Asegúrate de que Ollama esté corriendo y que el modelo 'llama3.2' esté descargado
llm = OllamaLLM(model="llama3")

# 4. Crear el Pipeline RAG con LangChain
# Definir un prompt para el LLM que incluya el contexto recuperado
prompt_template = PromptTemplate(
    template="""Usa el siguiente contexto para responder a la pregunta.
    Si no sabes la respuesta, di que no lo sabes, no intentes inventar una respuesta.

    Contexto: {context}
    Pregunta: {question}
    Respuesta útil:""",
    input_variables=["context", "question"],
)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", # "stuff" concatena todos los documentos en un solo prompt
    retriever=vector_db.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)

# 5. Realizar una Consulta RAG
query = "¿Qué es RAG y cómo funciona?"
response = rag_chain.invoke({"query": query})

print(f"Pregunta: {query}")
print(f"Respuesta: {response['result']}")
if response['source_documents']:
    print("\nDocumentos fuente:")
    for doc in response['source_documents']:
        print(f"- {doc.page_content[:100]}...") # Imprimir los primeros 100 caracteres del documento fuente
