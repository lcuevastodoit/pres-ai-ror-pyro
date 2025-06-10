import Pyro5.api, json
@Pyro5.api.expose
class MyClass:
    def __init__(self): self.other_data="other data"
    def ask_question(self,q): return json.dumps({"question":q,"answer":"AI Answer","other_data":self.other_data})
def main():
    daemon=Pyro5.api.Daemon()
    ns=Pyro5.api.locate_ns()
    uri=daemon.register(MyClass())
    ns.register("chatService1",uri)
    print(f"Ready. Registered as chatService1")
    daemon.requestLoop()
if __name__=="__main__": main()
