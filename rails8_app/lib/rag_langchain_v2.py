import os
import datetime
import glob
import signal
import sys
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
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser

@Pyro5.api.expose
class RAGChat:
    def __init__(self):
        self.log_message("Iniciando RAGChat con conexión a la base de datos SQLite")
        load_dotenv()
        default_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage/development.sqlite3")
        db_path = os.getenv("SQLITE_DB_PATH", default_db)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT question, answer FROM qa_pairs")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.log_message(f"Conectado a la base de datos SQLite: {db_path}")
        self.log_message(f"Preguntas y respuestas cargadas: {len(rows)} pares")
        docs = []
        docs = [Document(page_content=f"Q: {q}\nA: {a}") for q, a in rows]

        # Cargar documentos PDF
        self.log_message("Cargando documentos PDF...")
        pdf_docs = self._load_pdf_documents()
        docs.extend(pdf_docs)
        self.log_message(f"Documentos PDF cargados: {len(pdf_docs)} documentos")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        self.log_message(f"Documentos divididos en {len(chunks)} fragmentos")
        # Crear base de vectores FAISS
        embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(chunks, embed_model)
        self.log_message("Base de vectores FAISS creada")
        # Inicializar LLM y pipeline RAG
        llm = OllamaLLM(model="llama3-1b-q4km", num_ctx=4096, temperature=0, top_p=0.1)
        prompt = PromptTemplate(
            template="""Responde únicamente utilizando solo la información proporcionada en el contexto.
Si la respuesta no se encuentra en el contexto no la respondas, e indica claramente "Pregunta fuera de contexto".

Contexto: {context}
Pregunta: {question}
Respuesta:""",
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

    def _load_pdf_documents(self):
        """Cargar documentos PDF usando PyMuPDF4LLM"""
        pdf_docs = []

        # Definir directorio donde están los PDFs
        pdf_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage/pdfs")

        if os.path.exists(pdf_directory):
            # Buscar todos los archivos PDF en el directorio
            self.log_message(f"Buscando PDFs en el directorio: {pdf_directory}")
            pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

            for pdf_file in pdf_files:
                self.log_message(f"Procesando PDF: {pdf_file}")
                try:
                    # Crear loader para cada PDF
                    loader = PyMuPDF4LLMLoader(
                        file_path=pdf_file,
                        mode="page",
                        extract_images=True,
                        images_parser=TesseractBlobParser()
                    )

                    # Cargar documentos del PDF
                    pdf_documents = loader.load()
                    pdf_docs.extend(pdf_documents)

                except Exception as e:
                    print(f"Error procesando {pdf_file}: {e}")

        return pdf_docs

    def log_message(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] - {message}"
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../log/server.log")
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        with open(log_path, "a") as log_file:
            log_file.write(f"{message}\n")
        print(message)

    def shutdown(self):
        """Cleanup on process exit."""
        self.log_message("RAGChat server is shutting down...")

def main():
    daemon = Pyro5.api.Daemon()
    try:
        chat = RAGChat()
        ns = Pyro5.api.locate_ns()
        uri = daemon.register(chat)
        ns.register("RAGChat", uri)
        chat.log_message("RAGChat server is running...")
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda s, f: handle_exit(chat, daemon, s))
        daemon.requestLoop()
    except Exception as e:
        chat.log_message(f"Error iniciando RAGChat: {e}")

def handle_exit(chat, daemon, signum):
    chat.log_message(f"Received signal {signum}, shutting down…")
    try:
        daemon.shutdown()
    except:
        pass
    chat.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    main()
