import Pyro5.api

@Pyro5.api.expose
class Clase2:
    def saludo(self):
        return "Hola desde Clase2"
