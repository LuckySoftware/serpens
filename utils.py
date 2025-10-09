import sys, os

def resource_path(relative_path: str) -> str:
    """Obtiene la ruta válida para recursos, compatible con PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
