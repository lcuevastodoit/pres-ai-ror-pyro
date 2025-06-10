import sys,Pyro5.api
if len(sys.argv)<2: print("Uso: python client.py <question>",file=sys.stderr); exit(1)
question=sys.argv[1]
uri="PYRO:chatService1@localhost:9090"
obj=Pyro5.api.Proxy(uri)
print(obj.ask_question(question))
