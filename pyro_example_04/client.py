import sys
import Pyro5.api

if len(sys.argv) < 2:
    print("Uso: python cliente.py <objeto.metodo> o pyro.reload", file=sys.stderr)
    exit(1)

arg = sys.argv[1]

obj_control = Pyro5.api.Proxy("PYRONAME:server.control")

if arg == "reload":
    print(obj_control.reload_modules())
else:
    try:
        objeto_nombre, metodo_nombre = arg.split('.', 1)
    except ValueError:
        print("Formato incorrecto. Use <objeto.metodo>", file=sys.stderr)
        exit(1)
    resultado = obj_control.call(objeto_nombre, metodo_nombre)
    print(resultado)
