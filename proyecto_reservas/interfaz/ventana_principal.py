from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from clases.gestor_reservas import GestorReservas
from interfaz.ventana_disponibilidad import VentanaDisponibilidad


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏟️ Sistema de Reservas de Canchas Deportivas")
        self.setFixedSize(900, 600)

        self.gestor = GestorReservas()
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)

        # --- Título ---
        titulo = QLabel("Sistema de Reservas de Canchas Deportivas")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; margin: 10px;")
        layout.addWidget(titulo)

        # --- Botones principales ---
        botones = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Reserva")
        btn_eliminar = QPushButton("Eliminar Seleccionada")

        botones.addWidget(btn_agregar)
        botones.addWidget(btn_eliminar)
        layout.addLayout(botones)

        btn_agregar.clicked.connect(self.abrir_disponibilidad)
        btn_eliminar.clicked.connect(self.eliminar_reserva)

        # --- Tabla de reservas ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(
            ["Cliente", "Teléfono", "Cancha", "Fecha", "Hora", "Costo"]
        )
        layout.addWidget(self.tabla)

        self.setCentralWidget(central)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Recarga la tabla con las reservas actuales."""
        self.tabla.setRowCount(len(self.gestor.reservas))
        for i, r in enumerate(self.gestor.reservas):
            self.tabla.setItem(i, 0, QTableWidgetItem(r.cliente.nombre))
            self.tabla.setItem(i, 1, QTableWidgetItem(r.cliente.telefono))
            self.tabla.setItem(i, 2, QTableWidgetItem(r.cancha.nombre))
            self.tabla.setItem(i, 3, QTableWidgetItem(r.fecha))
            self.tabla.setItem(i, 4, QTableWidgetItem(r.hora))
            self.tabla.setItem(i, 5, QTableWidgetItem(f"${r.costo:,.0f}"))

    def eliminar_reserva(self):
        """Elimina la reserva seleccionada de la tabla."""
        fila = self.tabla.currentRow()
        if fila >= 0:
            self.gestor.eliminar_reserva(fila)
            QMessageBox.information(self, "Eliminada", "Reserva eliminada correctamente.")
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Atención", "Seleccione una reserva para eliminar.")

    def abrir_disponibilidad(self):
        """Abre la ventana para gestionar nuevas reservas."""
        ventana = VentanaDisponibilidad(self.gestor)
        ventana.exec()
        self.actualizar_tabla()
