from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from clases.gestor_reservas import GestorReservas
from clases.cliente import Cliente

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏟️ Sistema de Reservas de Canchas Deportivas")
        self.setFixedSize(800, 600)

        self.gestor = GestorReservas()
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)

        titulo = QLabel("Sistema de Reservas de Canchas Deportivas")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; margin: 10px;")

        form_layout = QHBoxLayout()
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre del cliente")
        self.telefono = QLineEdit()
        self.telefono.setPlaceholderText("Teléfono")

        self.cancha = QComboBox()
        for c in self.gestor.canchas:
            self.cancha.addItem(c.nombre)

        self.hora = QComboBox()
        self.hora.addItems([f"{h}:00" for h in range(10, 23)])

        form_layout.addWidget(self.nombre)
        form_layout.addWidget(self.telefono)
        form_layout.addWidget(self.cancha)
        form_layout.addWidget(self.hora)

        botones = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Reserva")
        btn_eliminar = QPushButton("Eliminar Seleccionada")
        botones.addWidget(btn_agregar)
        botones.addWidget(btn_eliminar)

        btn_agregar.clicked.connect(self.agregar_reserva)
        btn_eliminar.clicked.connect(self.eliminar_reserva)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Cliente", "Teléfono", "Cancha", "Hora"])
        self.actualizar_tabla()

        layout.addWidget(titulo)
        layout.addLayout(form_layout)
        layout.addLayout(botones)
        layout.addWidget(self.tabla)

        self.setCentralWidget(central)

    def agregar_reserva(self):
        try:
            cliente = Cliente(self.nombre.text(), self.telefono.text())
            cancha = next(c for c in self.gestor.canchas if c.nombre == self.cancha.currentText())
            hora = self.hora.currentText()
            self.gestor.agregar_reserva(cliente, cancha, hora)
            QMessageBox.information(self, "Éxito", "Reserva creada correctamente.")
            self.actualizar_tabla()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def eliminar_reserva(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            self.gestor.eliminar_reserva(fila)
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Atención", "Seleccione una reserva para eliminar.")

    def actualizar_tabla(self):
        self.tabla.setRowCount(len(self.gestor.reservas))
        for i, r in enumerate(self.gestor.reservas):
            self.tabla.setItem(i, 0, QTableWidgetItem(r.cliente.nombre))
            self.tabla.setItem(i, 1, QTableWidgetItem(r.cliente.telefono))
            self.tabla.setItem(i, 2, QTableWidgetItem(r.cancha.nombre))
            self.tabla.setItem(i, 3, QTableWidgetItem(r.hora))
