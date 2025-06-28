import argparse
import Pyro5.api

def main():
    parser = argparse.ArgumentParser(description="Cliente para probar RAGChat vía Pyro5")
    parser.add_argument("query", type=str, help="Consulta o pregunta para RAGChat")
    parser.add_argument("--uri", type=str, default="PYRONAME:RAGChat",
                        help="URI o nombre Pyro del objeto RAGChat (por defecto PYRONAME:RAGChat)")
    args = parser.parse_args()

    # Crear proxy Pyro usando URI o nombre
    chatbot = Pyro5.api.Proxy(args.uri)

    # Obtener respuesta para la consulta
    respuesta = chatbot.ask(args.query)
    print("Pregunta:", args.query)
    print("Respuesta:", respuesta)

if __name__ == "__main__":
    main()
