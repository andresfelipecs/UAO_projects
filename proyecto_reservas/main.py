import sys
from PyQt6.QtWidgets import QApplication
from interfaz.ventana_principal import VentanaPrincipal

app = QApplication(sys.argv)
with open("interfaz/estilos.qss", "r") as f:
    app.setStyleSheet(f.read())

ventana = VentanaPrincipal()
ventana.show()
sys.exit(app.exec())
