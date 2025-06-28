require 'open3'

class AiClient
  PYTHON_PATH = 'python3'
  CLIENT_PATH = File.expand_path('../client2.py', __FILE__)

  def self.ask(question)
    cmd = [PYTHON_PATH, CLIENT_PATH, question.to_s]
    stdout, stderr, status = Open3.capture3(*cmd)
    if status.success?
      # Extrae solo la línea de respuesta
      if stdout =~ /Respuesta:\s*(.+)/
        $1.strip
      else
        stdout.strip
      end
    else
      raise "AIClient error: #{stderr.presence || 'Unknown error'}"
    end
  end
end
