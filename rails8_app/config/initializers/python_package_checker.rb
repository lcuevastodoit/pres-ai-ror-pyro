require "open3"

class PythonPackageChecker
  REQUIRED_PACKAGES = [
    "hf_xet",
    "dotenv",
    "sentence-transformers",
    "torch",
    "Pyro5",
    "langchain",
    "langchain_community",
    "langchain-huggingface",
    "langchain-ollama",
    "langchain-pymupdf4llm",
    "faiss-cpu",
    "ollama",
    "llama-cpp-python",
    "pypdf",
    '"numpy<2"',
    '"huggingface_hub[cli]"',
    "scikit-learn",
    "redis",
    "langdetect",
    "sacremoses",
    "psycopg2"
  ].freeze

  def self.ensure_packages_installed
    REQUIRED_PACKAGES.each do |package|
      unless package_installed?(package)
        install_package(package)
      end
    end
    model_path = Rails.root.join("lib", "Llama-3.2-1B-Instruct-Q4_K_M.gguf")
    download_model unless File.exist?(model_path)
  end

  def self.download_model
    puts "Descargando el modelo Llama-3.2-1B-Instruct-Q4_K_M.gguf desde Hugging Face..."
    lib_dir = Rails.root.join("lib")
    system("huggingface-cli download bartowski/Llama-3.2-1B-Instruct-GGUF --include \"Llama-3.2-1B-Instruct-Q4_K_M.gguf\" --local-dir #{lib_dir}")
    ollama_there = system("ollama list | grep llama3-1b-q4km")
    modelfile_path = Rails.root.join("lib", "Modelfile")
    system("ollama create llama3-1b-q4km -f #{modelfile_path}") unless ollama_there
  end

  def self.package_installed?(package)
    stdout, _stderr, status = Open3.capture3("pip show #{package}")
    if status.success?
      puts "Paquete #{package} ya está instalado."
      true
    else
      false
    end
  end

  def self.install_package(package)
    puts "Instalando paquete Python: #{package}..."
    stdout, stderr, status = Open3.capture3("pip install #{package}")
    if status.success?
      puts "Paquete #{package} instalado correctamente."
    else
      puts "Error al instalar el paquete #{package}: #{stderr}"
    end
  end
end

PythonPackageChecker.ensure_packages_installed
