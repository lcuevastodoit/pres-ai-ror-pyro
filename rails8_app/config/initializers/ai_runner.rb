require 'open3'

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
          uri = ns.lookup("AIChat")
          print("OK")
      except Exception:
          pass
    PYTHON
    output.include?("OK")
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

if pyro5_server_running?
  puts "[Pyro5] Servidor AIChat ya está corriendo."
else
  puts "[Pyro5] Servidor AIChat no está corriendo. Iniciando..."
  server_path = "#{Rails.root}/lib/server.py"
  @pyro_server_pid = spawn("python3 #{server_path}", out: "tmp/pyro5_server.log", err: "tmp/pyro5_server.log")
  puts "[Pyro5] Servidor AIChat iniciado con PID #{@pyro_server_pid}."
end

at_exit do
  if @pyro_server_pid
    puts "[Pyro5] Terminando servidor AIChat (PID #{@pyro_server_pid})..."
    Process.kill("TERM", @pyro_server_pid) rescue nil
  end
  if @pyro_nameserver_pid
    puts "[Pyro5] Terminando NameServer (PID #{@pyro_nameserver_pid})..."
    Process.kill("TERM", @pyro_nameserver_pid) rescue nil
  end
end
