import Pyro5.api

@Pyro5.api.expose
class Clase3:
    def saludo(self):
        return "Hola desde Clase3"
