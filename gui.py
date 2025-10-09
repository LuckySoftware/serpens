from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTextEdit, QListWidget, QMessageBox, QStackedWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QIcon, QPixmap

from finance import (
    calcular_van,
    margen_contribucion_unitario,
    margen_contribucion_porcentual,
    punto_equilibrio_unidades
)
from utils import resource_path


class FinanzasApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serpens - Calculadora Financiera")
        self.resize(900, 600)
        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # ===== Menú lateral =====
        menu = QWidget()
        menu_layout = QVBoxLayout()
        menu.setLayout(menu_layout)
        menu.setFixedWidth(250)
        menu.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: white;
                font-size: 14px;
            }
        """)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(resource_path("assets/logo.png"))
        logo_label.setPixmap(pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Serpens")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; margin-bottom: 10px;")

        # Menú
        self.menu_list = QListWidget()
        self.menu_list.addItem(QListWidgetItem("💰 Valor Presente Neto (VAN)"))
        self.menu_list.addItem(QListWidgetItem("📈 Margen de Contribución"))
        self.menu_list.addItem(QListWidgetItem("⚖️ Punto de Equilibrio"))
        self.menu_list.currentRowChanged.connect(self._cambiar_vista)
        self.menu_list.setStyleSheet("""
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
                border-radius: 6px;
            }
        """)

        menu_layout.addWidget(logo_label)
        menu_layout.addWidget(title_label)
        menu_layout.addWidget(self.menu_list)
        menu_layout.addStretch()

        # ===== Panel principal =====
        self.stacked = QStackedWidget()
        self.stacked.addWidget(self._vista_van())
        self.stacked.addWidget(self._vista_margen())
        self.stacked.addWidget(self._vista_equilibrio())

        main_layout.addWidget(menu)
        main_layout.addWidget(self.stacked, 1)
        self._set_dark_theme()

    def _set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2B2B2B"))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor("#383838"))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

    # ===== Vistas =====
    def _vista_van(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        title = QLabel("💰 Cálculo del Valor Presente Neto (VAN)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(title)

        self.input_flujos = QLineEdit()
        self.input_tasa = QLineEdit()
        self.input_inversion = QLineEdit()
        self.result_van = QTextEdit()
        self.result_van.setReadOnly(True)

        self.input_flujos.setPlaceholderText("Flujos: 2000, 3000, 4000")
        self.input_tasa.setPlaceholderText("Tasa de descuento (%)")
        self.input_inversion.setPlaceholderText("Inversión inicial")

        btn = QPushButton("Calcular VAN")
        btn.clicked.connect(self._calcular_van)
        btn.setStyleSheet("background-color:#4CAF50;color:white;font-weight:bold;border-radius:6px;")

        for i in [self.input_flujos, self.input_tasa, self.input_inversion, btn, self.result_van]:
            layout.addWidget(i)
        return w

    def _vista_margen(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        title = QLabel("📈 Cálculo del Margen de Contribución")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(title)

        self.input_precio = QLineEdit()
        self.input_costo_var = QLineEdit()
        self.result_margen = QTextEdit()
        self.result_margen.setReadOnly(True)

        self.input_precio.setPlaceholderText("Precio de venta por unidad")
        self.input_costo_var.setPlaceholderText("Costo variable por unidad")

        btn = QPushButton("Calcular Margen")
        btn.clicked.connect(self._calcular_margen)
        btn.setStyleSheet("background-color:#4CAF50;color:white;font-weight:bold;border-radius:6px;")

        for i in [self.input_precio, self.input_costo_var, btn, self.result_margen]:
            layout.addWidget(i)
        return w

    def _vista_equilibrio(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        title = QLabel("⚖️ Cálculo del Punto de Equilibrio")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(title)

        self.input_cf = QLineEdit()
        self.input_precio_eq = QLineEdit()
        self.input_costo_eq = QLineEdit()
        self.result_eq = QTextEdit()
        self.result_eq.setReadOnly(True)

        self.input_cf.setPlaceholderText("Costos fijos totales")
        self.input_precio_eq.setPlaceholderText("Precio de venta por unidad")
        self.input_costo_eq.setPlaceholderText("Costo variable por unidad")

        btn = QPushButton("Calcular Punto de Equilibrio")
        btn.clicked.connect(self._calcular_equilibrio)
        btn.setStyleSheet("background-color:#4CAF50;color:white;font-weight:bold;border-radius:6px;")

        for i in [self.input_cf, self.input_precio_eq, self.input_costo_eq, btn, self.result_eq]:
            layout.addWidget(i)
        return w

    # ===== Funciones =====
    def _cambiar_vista(self, index: int):
        self.stacked.setCurrentIndex(index)

    def _calcular_van(self):
        from finance import calcular_van
        try:
            flujos = [float(x.strip()) for x in self.input_flujos.text().split(",")]
            tasa = float(self.input_tasa.text())
            inv = float(self.input_inversion.text())
            van = calcular_van(flujos, tasa, inv)
            msg = f"VAN = {van:.2f}\n\n{'Proyecto rentable ✅' if van > 0 else 'Proyecto no rentable ❌'}"
            self.result_van.setText(msg)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _calcular_margen(self):
        from finance import margen_contribucion_unitario, margen_contribucion_porcentual
        try:
            p = float(self.input_precio.text())
            c = float(self.input_costo_var.text())
            mu = margen_contribucion_unitario(p, c)
            mp = margen_contribucion_porcentual(p, c)
            self.result_margen.setText(f"Margen unitario: {mu:.2f}\nMargen porcentual: {mp:.2f}%")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _calcular_equilibrio(self):
        from finance import punto_equilibrio_unidades
        try:
            cf = float(self.input_cf.text())
            pv = float(self.input_precio_eq.text())
            cv = float(self.input_costo_eq.text())
            unidades = punto_equilibrio_unidades(cf, pv, cv)
            self.result_eq.setText(f"Punto de equilibrio: {unidades:.2f} unidades")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
