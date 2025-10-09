
# Serpens • Calculadora Financiera

![Logo de Serpens](https://github.com/user-attachments/assets/3a79b0fa-cf8a-47dd-82db-f2570bb9e4a1)

**Serpens** es una calculadora financiera de escritorio con una interfaz gráfica (GUI) moderna e intuitiva, diseñada para simplificar el cálculo de indicadores clave como el **Valor Actual Neto (VAN)**, el **Margen de Contribución** y el **Punto de Equilibrio**.

Desarrollada en Python, es la herramienta ideal para profesionales de las finanzas, emprendedores que necesitan tomar decisiones basadas en datos y estudiantes de economía o administración.

## Características Principales

* **Interfaz Moderna e Intuitiva**: Diseñada para ser fácil de usar, sin necesidad de conocimientos técnicos previos.
* **Cálculos Financieros Clave**:
    * **VAN (Valor Actual Neto)**: Evalúa la rentabilidad y viabilidad de una inversión a futuro.
    * **Margen de Contribución**: Mide cómo un producto o servicio contribuye a la rentabilidad de la empresa.
    * **Punto de Equilibrio**: Determina el nivel de ventas necesario para cubrir todos los costos fijos y variables.
* **Diseño UI/UX Profesional**: Cada elemento, desde los colores hasta la tipografía, ha sido cuidadosamente seleccionado para garantizar la máxima claridad y comodidad visual.
* **Lista para Distribuir**: Empaquetada con **PyInstaller** para generar un ejecutable (`.exe`) sencillo de distribuir en sistemas Windows.

## Tecnologías Utilizadas

* **Python 3.10+**
* **PyQt6 / PySide6** para la interfaz gráfica.
* **PyInstaller** para el empaquetado de la aplicación.
* **pytest** para las pruebas unitarias.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera para mantener el código limpio y escalable:

```

Serpens/
│
├── assets/                   \# Recursos gráficos (logos, íconos)
│   ├── logo.png
│   └── logo.ico
│
├── gui.py                    \# Lógica y estructura de la interfaz gráfica
├── finance.py                \# Módulo con las funciones de cálculo financiero
├── utils.py                  \# Funciones auxiliares y de validación
├── main.py                   \# Punto de entrada para ejecutar la aplicación
│
├── tests/                    \# Carpeta de tests unitarios
│   └── test\_finance.py       \# Pruebas para las fórmulas financieras
│
├── requirements.txt          \# Lista de dependencias de Python
├── README.md                 \# Documentación del proyecto
└── build\_serpens.bat         \# (Opcional) Script para automatizar la compilación en Windows

````

---

## Instalación y Uso

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

### **Requisitos Previos**

Asegúrate de tener instalado:
* [Python 3.10 o superior](https://www.python.org/downloads/)
* `pip` (generalmente viene incluido con Python)

### **Pasos de Instalación**

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/Serpens.git](https://github.com/tu-usuario/Serpens.git)
    cd Serpens
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    Todas las librerías necesarias se encuentran en el archivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    Una vez instaladas las dependencias, puedes iniciar la calculadora con el siguiente comando:
    ```bash
    python main.py
    ```

---

## Generar el Ejecutable (`.exe`) con PyInstaller

Para distribuir **Serpens** como una aplicación de escritorio independiente en Windows, puedes usar PyInstaller.

### **1. Instalar PyInstaller**

Si no lo tienes instalado, abre tu terminal y ejecuta:
```bash
pip install pyinstaller
````

### **2. Generar el archivo `.exe`**

El siguiente comando compilará todo el proyecto en un único archivo ejecutable. Ubícate en la raíz del proyecto y ejecuta:

```bash
pyinstaller --name "Serpens" --onefile --windowed --icon="assets/logo.ico" main.py
```

**Desglose del comando:**

  * `--name "Serpens"`: Asigna el nombre "Serpens" al archivo ejecutable final.
  * `--onefile`: Empaqueta todo (código, dependencias y assets) en un **único archivo `.exe`**.
  * `--windowed`: Evita que se abra una consola de comandos en segundo plano al ejecutar la aplicación.
  * `--icon="assets/logo.ico"`: Asigna el ícono personalizado a tu ejecutable.
  * `main.py`: Especifica el punto de entrada de la aplicación.

Una vez finalizado el proceso, encontrarás el archivo `Serpens.exe` dentro de una nueva carpeta llamada `dist`.

> **Alternativa:** Puedes usar el script `build_serpens.bat` (si lo tienes configurado) para automatizar este proceso con un solo clic en Windows.

## Pruebas (Testing)

Para asegurar la fiabilidad de los cálculos financieros, el proyecto incluye pruebas unitarias. Para ejecutarlas, puedes usar `pytest`:

```bash
pytest tests/
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar **Serpens**, por favor sigue estos pasos:

1.  Haz un "Fork" del proyecto.
2.  Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3.  Realiza tus cambios y haz "Commit" (`git commit -m 'Agrega nueva funcionalidad'`).
4.  Haz "Push" a la rama (`git push origin feature/nueva-funcionalidad`).
5.  Abre un "Pull Request".

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
