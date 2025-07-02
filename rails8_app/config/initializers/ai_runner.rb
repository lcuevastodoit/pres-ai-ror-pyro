require 'open3'
if defined?(Rails::Server)
  @pyro_nameserver_pid = nil
  @pyro_server_pid = nil

  def nameserver_running?
    begin
      output, status = Open3.capture2("python3", "-c", <<~PYTHON)
        import Pyro5.api
        try:
            ns = Pyro5.api.locate_ns()
            print("OK")
        except Exception:
            pass
      PYTHON
      output.include?("OK")
    rescue
      false
    end
  end

  def pyro5_server_running?
    begin
      output, status = Open3.capture2("python3", "-c", <<~PYTHON)
        import Pyro5.api
        try:
            ns = Pyro5.api.locate_ns()
            uri = ns.lookup("RAGChat")
            print("OK")
        except Exception:
            pass
      PYTHON
      output.include?("OK")
    rescue
      false
    end
  end

  def ollama_running?
    begin
      output, status = Open3.capture2("ps aux | grep -v grep | grep 'ollama serve'")
      output.include?("ollama serve")
    rescue
      false
    end
  end

  if nameserver_running?
    puts "[Pyro5] NameServer ya está corriendo."
  else
    puts "[Pyro5] NameServer no está corriendo. Iniciando..."
    @pyro_nameserver_pid = spawn("python3 -m Pyro5.nameserver", out: "tmp/pyro5_nameserver.log", err: "tmp/pyro5_nameserver.log")
    puts "[Pyro5] NameServer iniciado con PID #{@pyro_nameserver_pid}."
    sleep 5
  end

  if ollama_running?
    puts "[Ollama] Ollama ya está corriendo."
  else
    puts "[Ollama] Ollama no está corriendo. Iniciando..."
    @ollama_pid = spawn("ollama serve", out: "tmp/ollama.log", err: "tmp/ollama.log")
    puts "[Ollama] Ollama iniciado con PID #{@ollama_pid}."
  end

  if pyro5_server_running?
    puts "[Pyro5] Servidor RAGChat ya está corriendo."
  else
    puts "[Pyro5] Servidor RAGChat no está corriendo. Iniciando..."
    server_path = "#{Rails.root}/lib/rag_langchain_v2.py"
    @pyro_server_pid = spawn("python3 #{server_path}", out: "tmp/pyro5_server.log", err: "tmp/pyro5_server.log")
    puts "[Pyro5] Servidor RAGChat iniciado con PID #{@pyro_server_pid}."
  end

  at_exit do
    if @pyro_server_pid
      puts "[Pyro5] Terminando servidor RAGChat (PID #{@pyro_server_pid})..."
      Process.kill("TERM", @pyro_server_pid) rescue nil
    end
    if @pyro_nameserver_pid
      puts "[Pyro5] Terminando NameServer (PID #{@pyro_nameserver_pid})..."
      Process.kill("TERM", @pyro_nameserver_pid) rescue nil
    end
    if @ollama_pid
      puts "[Ollama] Terminando Ollama (PID #{@ollama_pid})..."
      Process.kill("TERM", @ollama_pid) rescue nil
    end
    puts "[Pyro5] Todos los procesos han sido terminados."
    puts "[Ollama] Todos los procesos han sido terminados."
    puts "[Rails] Aplicación cerrada correctamente."
    puts "[Rails] Rails server will be stopped now."
  end
end
