import Pyro5.api

@Pyro5.api.expose
class Clase1:
    def saludo(self):
        return "Hola desde Clase1"
