import Pyro5.api
import importlib
import clase1
import clase2
import clase3

@Pyro5.api.expose
class ServerControl:
    def __init__(self):
        self.reload_modules()

    def reload_modules(self):
        importlib.reload(clase1)
        importlib.reload(clase2)
        importlib.reload(clase3)
        self.objeto1 = clase1.Clase1()
        self.objeto2 = clase2.Clase2()
        self.objeto3 = clase3.Clase3()
        print("Loaded!")
        return "Loaded!"

    # Para facilitar llamadas dinámicas a objetos y métodos
    def call(self, objeto_nombre, metodo_nombre):
        obj = getattr(self, objeto_nombre, None)
        if obj is None:
            return f"Objeto '{objeto_nombre}' no encontrado"
        if not hasattr(obj, metodo_nombre):
            return f"Método '{metodo_nombre}' no encontrado en '{objeto_nombre}'"
        metodo = getattr(obj, metodo_nombre)
        return metodo()

def main():
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    server = ServerControl()
    uri = daemon.register(server)
    ns.register("server.control", uri)
    print(f"Servidor listo y registrado como 'server.control'")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
