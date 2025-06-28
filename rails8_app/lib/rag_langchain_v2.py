import os
import sqlite3
import Pyro5.api
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

@Pyro5.api.expose
class RAGChat:
    def __init__(self):
        # Carga de .env y conexión a la misma BD SQLite usada en server.py
        load_dotenv()
        default_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage/development.sqlite3")
        db_path = os.getenv("SQLITE_DB_PATH", default_db)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT question, answer FROM qa_pairs")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Construcción de documentos y fragmentación
        docs = [Document(page_content=f"Q: {q}\nA: {a}") for q, a in rows]
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # Crear base de vectores FAISS
        embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(chunks, embed_model)

        # Inicializar LLM y pipeline RAG
        llm = OllamaLLM(model="llama3")
        prompt = PromptTemplate(
            template="""Usa el siguiente contexto para responder a la pregunta.
Si no sabes la respuesta, di que no lo sabes.

Contexto: {context}
Pregunta: {question}
Respuesta útil:""",
            input_variables=["context", "question"]
        )
        self.rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(),
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt}
        )

    def ask(self, query: str) -> str:
        # Ejecutar la consulta RAG y devolver el resultado
        result = self.rag_chain.invoke({"query": query})
        return result["result"]

def main():
    chat = RAGChat()
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(chat)
    ns.register("RAGChat", uri)
    print("RAGChat server is running...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()