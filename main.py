import sys
import time
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer

from gui import FinanzasApp
from utils import resource_path


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # === Splash screen ===
    splash_pix = QPixmap(resource_path("assets/logo.png"))
    splash = QSplashScreen(splash_pix.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
    splash.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SplashScreen)
    splash.showMessage(
        "\n\n💼 Serpens\n\nCargando módulos...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white
    )
    splash.show()

    app.processEvents()

    # Simular carga (puedes cambiar el tiempo)
    time.sleep(2)

    ventana = FinanzasApp()
    ventana.show()
    splash.finish(ventana)

    sys.exit(app.exec())
