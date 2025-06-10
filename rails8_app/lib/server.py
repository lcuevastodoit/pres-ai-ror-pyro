import os
import sqlite3
import torch
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
import Pyro5.api

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@Pyro5.api.expose
class AIChat:
    def __init__(self):
        load_dotenv()
        db_path = os.getenv(
            "SQLITE_DB_PATH",
            os.path.join(get_project_root(), "storage", "development.sqlite3")
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
        # self.model = SentenceTransformer('all-mpnet-base-v2', device=self.device)
        # self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device=self.device)
        # self.model = SentenceTransformer('nli-roberta-base-v2', device=self.device)
        self._load_data()

    def _load_data(self):
        self.cursor.execute("SELECT question, answer FROM qa_pairs")
        rows = self.cursor.fetchall()
        self.questions, self.answers = zip(*rows) if rows else ([], [])
        # Separar por idioma
        self.questions_en = [q for q in self.questions if q.isascii()]
        self.answers_en = [a for q, a in zip(self.questions, self.answers) if q.isascii()]
        self.questions_es = [q for q in self.questions if not q.isascii()]
        self.answers_es = [a for q, a in zip(self.questions, self.answers) if not q.isascii()]
        # Generar embeddings en memoria
        self.embeddings_en = self.model.encode(self.questions_en, convert_to_tensor=True, device=self.device) if self.questions_en else None
        self.embeddings_es = self.model.encode(self.questions_es, convert_to_tensor=True, device=self.device) if self.questions_es else None
        self.cursor.close()
        self.conn.close()

    def get_prediction(self, query):
        if not self.questions:
            return "No hay preguntas disponibles."
        query_emb = self.model.encode(
            query,
            convert_to_tensor=True,
            device=self.device,
            normalize_embeddings=True,  # ¡Nuevo parámetro clave!
            batch_size=18,  # Ajustar según tu hardware
            show_progress_bar=False
        )
        threshold = 0.65

        def buscar_similaridad(embeddings, answers):
            if embeddings is None or len(embeddings) == 0:
                return None, 0
            similitudes = util.cos_sim(query_emb, embeddings).squeeze()
            max_idx = similitudes.argmax().item()
            max_sim = similitudes[max_idx].item()
            return answers[max_idx] if max_sim >= threshold else None, max_sim

        respuesta, sim = buscar_similaridad(self.embeddings_en, self.answers_en)
        if respuesta:
            return respuesta
        respuesta, sim = buscar_similaridad(self.embeddings_es, self.answers_es)
        if respuesta:
            return respuesta
        return "Reformule su pregunta o intente con otra diferente."

    def close(self):
        print("Goodbye!")

def main():
    chatbot = AIChat()
    daemon = Pyro5.api.Daemon()
    ns=Pyro5.api.locate_ns()
    uri = daemon.register(chatbot)
    ns.register("AIChat",uri)
    print(f"Ready. Registered as AIChat")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
