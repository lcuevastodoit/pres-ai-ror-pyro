require "open3"

class PythonPackageChecker
  REQUIRED_PACKAGES = [
    "dotenv",
    "sentence-transformers",
    "torch",
    "Pyro5"
  ].freeze

  def self.ensure_packages_installed
    REQUIRED_PACKAGES.each do |package|
      unless package_installed?(package)
        install_package(package)
      end
    end
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
