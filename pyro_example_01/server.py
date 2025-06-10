import Pyro5.api,json
@Pyro5.api.expose
class MyClass:
    def __init__(self): self.other_data="other data"
    def ask_question(self,q): return json.dumps({"question":q,"answer":"AI Answer","other_data":self.other_data})
def main():
    daemon=Pyro5.api.Daemon(host="localhost",port=9090)  # Puerto fijo
    uri=daemon.register(MyClass(),objectId="chatService1")  # URI fija con objectId
    print(f"Ready. Object uri = {uri}")
    daemon.requestLoop()
if __name__=="__main__": main()
