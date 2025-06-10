import Pyro5.api
from clase1 import Clase1
from clase2 import Clase2
from clase3 import Clase3

def main():
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()

    obj1 = Clase1()
    uri1 = daemon.register(obj1)
    ns.register("objeto1", uri1)

    obj2 = Clase2()
    uri2 = daemon.register(obj2)
    ns.register("objeto2", uri2)

    obj3 = Clase3()
    uri3 = daemon.register(obj3)
    ns.register("objeto3", uri3)

    print("Objetos registrados: objeto1, objeto2, objeto3")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
