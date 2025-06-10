require 'open3'

if ARGV.length < 1
  warn "Uso: ruby client.rb <objeto.metodo>"
  exit 1
end

invocacion = ARGV[0]  # Ejemplo: "objeto1.saludo"
out, err, status = Open3.capture3("python3 client.py #{invocacion}")

if status.success?
  puts out
else
  warn "Error ejecutando cliente Python: #{err}"
end
