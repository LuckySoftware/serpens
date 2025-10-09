@echo off
:: ------------------------------
:: Build script para Serpens
:: ------------------------------

echo 🐍 Iniciando build de Serpens...

:: Ir a la carpeta raíz del proyecto
cd /d %~dp0\..

:: Limpiar builds previos
echo 🧹 Limpiando carpetas previas...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Serpens.spec del Serpens.spec
if exist __pycache__ rmdir /s /q __pycache__

:: Instalar dependencias (opcional)
echo 📦 Instalando dependencias...
pip install -r requirements.txt

:: Empaquetar con PyInstaller
echo 🚀 Empaquetando Serpens.exe...
python -m PyInstaller --noconfirm --onefile --windowed main.py --name "Serpens" --add-data "assets;assets" --icon=assets/logo.ico

:: Abrir carpeta con el ejecutable
echo ✅ Build completado. Abriendo carpeta dist...
start dist

pause
