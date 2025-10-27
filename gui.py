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
        self.van_flow_inputs = []
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
        palette.setColor(QPalette.ColorRole.Base, QColor("#383838")) # Funciona bien para QTextEdit
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        
        # --- AÑADIR ESTA LÍNEA ---
        # Define un color para el texto de ejemplo (ej. "Flujos: 2000...")
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#999999"))
        
        self.setPalette(palette)

        # --- AÑADIR ESTE BLOQUE ---
        # Forzamos el estilo de QLineEdit, que no toma bien la paleta.
        # Esto también aplica a los QLineEdit en las otras pestañas.
        self.setStyleSheet("""
            QLineEdit {
                background-color: #383838;
                color: white;
                border: 1px solid #555; /* Un borde sutil */
                padding: 5px;
                border-radius: 4px;
            }

            /* Opcional: Resaltar el campo cuando está seleccionado */
            QLineEdit:focus {
                border: 1px solid #4CAF50; /* Borde verde al seleccionar */
            }
        """)

    # ===== Vistas =====
    def _vista_van(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(10) # Añade espacio entre widgets

        title = QLabel("💰 Cálculo del Valor Presente Neto (VAN)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(title)

        # --- Layout para Años ---
        anos_layout = QHBoxLayout()
        anos_label = QLabel("Número de Años:")
        anos_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        self.input_anos_van = QLineEdit()
        self.input_anos_van.setPlaceholderText("Ej: 3")
        
        btn_generar = QPushButton("Generar Campos")
        btn_generar.clicked.connect(self._generar_campos_flujo)
        # Damos un estilo al botón de generar
        btn_generar.setStyleSheet("background-color:#555;color:white;border-radius:6px;padding:5px;")

        anos_layout.addWidget(anos_label)
        anos_layout.addWidget(self.input_anos_van)
        anos_layout.addWidget(btn_generar)
        
        layout.addLayout(anos_layout)

        # --- Contenedor para Flujos Dinámicos ---
        # Este QWidget contendrá los QLineEdit de los flujos
        self.flujos_container = QWidget()
        self.flujos_layout = QVBoxLayout(self.flujos_container)
        self.flujos_layout.setContentsMargins(0, 5, 0, 5) # Margen
        layout.addWidget(self.flujos_container)

        # --- Inputs Fijos (Tasa e Inversión) ---
        self.input_tasa = QLineEdit()
        self.input_inversion = QLineEdit()
        self.result_van = QTextEdit()
        self.result_van.setReadOnly(True)

        self.input_tasa.setPlaceholderText("Tasa de descuento (%) (ej: 10)")
        self.input_inversion.setPlaceholderText("Inversión inicial (ej: 500000)")

        btn = QPushButton("Calcular VAN")
        btn.clicked.connect(self._calcular_van)
        btn.setStyleSheet("background-color:#4CAF50;color:white;font-weight:bold;border-radius:6px;padding:5px;") # Añadido padding

        layout.addWidget(self.input_tasa)
        layout.addWidget(self.input_inversion)
        layout.addWidget(btn)
        layout.addWidget(self.result_van, 1) # El '1' hace que se expanda

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
        from finance import calcular_van # Es mejor mover estos imports al inicio del archivo
        try:
            # --- SECCIÓN MODIFICADA ---
            if not self.van_flow_inputs:
                 raise ValueError("Primero debe generar los campos de flujo.")
            
            flujos = []
            for i, campo_flujo in enumerate(self.van_flow_inputs):
                flujo_text = campo_flujo.text().strip()
                if not flujo_text:
                    # Lanza error si un campo está vacío
                    raise ValueError(f"El campo 'Flujo Año {i + 1}' no puede estar vacío.")
                flujos.append(float(flujo_text))
            # --- FIN DE SECCIÓN MODIFICADA ---

            tasa = float(self.input_tasa.text())
            inv = float(self.input_inversion.text())
            
            van = calcular_van(flujos, tasa, inv)
            msg = f"VAN = {van:.2f}\n\n{'Proyecto rentable ✅' if van > 0 else 'Proyecto no rentable ❌'}"
            self.result_van.setText(msg)
            
        except Exception as e:
            # Damos un mensaje de error más específico
            QMessageBox.warning(self, "Error de Cálculo", f"Error al calcular: {e}")

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

    def _generar_campos_flujo(self):
        # 1. Limpiar campos anteriores del layout
        # Iteramos en reversa para eliminar widgets de forma segura
        for i in reversed(range(self.flujos_layout.count())): 
            widget = self.flujos_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        # 2. Limpiar nuestra lista de referencia
        self.van_flow_inputs.clear()

        try:
            # 3. Obtener el número de años
            num_anos = int(self.input_anos_van.text())

            if num_anos <= 0:
                raise ValueError("El número de años debe ser positivo.")
            if num_anos > 50: # Límite razonable
                raise ValueError("El límite es 50 años.")

            # 4. Crear y añadir los nuevos campos
            for i in range(num_anos):
                flujo_input = QLineEdit()
                flujo_input.setPlaceholderText(f"Flujo del Año {i + 1}")
                
                # Añadir al layout y a nuestra lista
                self.flujos_layout.addWidget(flujo_input)
                self.van_flow_inputs.append(flujo_input)

        except Exception as e:
            QMessageBox.warning(self, "Error de Años", f"Por favor, ingrese un número válido.\n{e}")