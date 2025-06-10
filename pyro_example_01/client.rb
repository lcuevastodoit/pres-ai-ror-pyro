require 'json'; require 'open3'
question="¿Cuál es la respuesta a la vida?"
out, err, st = Open3.capture3("python3 client.py \"#{question}\"")
puts st.success? ? JSON.parse(out) : warn("Error: #{err}")