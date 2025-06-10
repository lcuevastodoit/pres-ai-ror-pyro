import sys
import Pyro5.api

if len(sys.argv) < 2:
    print("Uso: python client.py <objeto.metodo>", file=sys.stderr)
    exit(1)

# Recibe argumento tipo "objeto1.saludo"
arg = sys.argv[1]

try:
    objeto_nombre, metodo_nombre = arg.split('.', 1)
except ValueError:
    print("Formato incorrecto. Use <objeto.metodo>", file=sys.stderr)
    exit(1)

uri = f"PYRONAME:{objeto_nombre}"
obj = Pyro5.api.Proxy(uri)

# Llama dinámicamente al método indicado
if not hasattr(obj, metodo_nombre):
    print(f"El objeto '{objeto_nombre}' no tiene el método '{metodo_nombre}'", file=sys.stderr)
    exit(1)

metodo = getattr(obj, metodo_nombre)  # ruby equivalent: obj.send(metodo_nombre)
resultado = metodo()
print(resultado)
