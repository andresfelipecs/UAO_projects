from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QCalendarWidget, QListWidget,
    QPushButton, QMessageBox, QInputDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt, QDate
from clases.cliente import Cliente


class VentanaDisponibilidad(QDialog):
    def __init__(self, gestor):
        super().__init__()
        self.setWindowTitle("📅 Disponibilidad de Canchas")
        self.setFixedSize(480, 650)
        self.gestor = gestor

        self.fecha_seleccionada = QDate.currentDate().toString("yyyy-MM-dd")
        self.cancha_seleccionada = None
        self.hora_seleccionada = None

        layout = QVBoxLayout(self)

        # === Paso 1: Fecha ===
        label_fecha = QLabel("1️⃣ Seleccione una fecha:")
        label_fecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_fecha)

        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.calendario.setMinimumDate(QDate.currentDate())  # 🔒 Evita fechas pasadas
        layout.addWidget(self.calendario)

        # === Paso 2: Cancha ===
        self.label_cancha = QLabel("2️⃣ Seleccione una cancha:")
        self.label_cancha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_cancha)

        # Contenedor para botones de canchas
        self.botones_cancha = []
        botones_layout = QHBoxLayout()

        for c in self.gestor.canchas:
            boton = QPushButton(c.nombre)
            boton.setCheckable(True)
            boton.setStyleSheet(self.estilo_boton_apagado())
            boton.clicked.connect(self.seleccionar_cancha)
            self.botones_cancha.append(boton)
            botones_layout.addWidget(boton)

        layout.addLayout(botones_layout)

        # === Paso 3: Costo y horas ===
        self.label_costo = QLabel("Costo: $0 COP")
        self.label_costo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_costo.setStyleSheet("font-weight: bold; color: #88C0D0;")
        layout.addWidget(self.label_costo)

        self.label_horas = QLabel("3️⃣ Seleccione una hora disponible:")
        self.label_horas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_horas)

        self.lista_horas = QListWidget()
        layout.addWidget(self.lista_horas)

        # === Paso 4: Confirmar ===
        self.boton_confirmar = QPushButton("Confirmar Reserva ✅")
        self.boton_confirmar.setEnabled(False)
        self.boton_confirmar.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:disabled {
                background-color: #4C566A;
                color: #A0A0A0;
            }
        """)
        self.boton_confirmar.clicked.connect(self.confirmar_reserva)
        layout.addWidget(self.boton_confirmar)

        # Conexiones
        self.calendario.selectionChanged.connect(self.actualizar_fecha)
        self.lista_horas.itemClicked.connect(self.seleccionar_hora)


    # ==================================================
    #                FUNCIONES DE ESTILO
    # ==================================================

    def estilo_boton_apagado(self):
        return """
            QPushButton {
                background-color: #3B4252;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4C566A;
            }
        """

    def estilo_boton_encendido(self):
        return """
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                border: 2px solid #88C0D0;
            }
        """

    # ==================================================
    #                   FUNCIONALIDAD
    # ==================================================

    def actualizar_fecha(self):
        """Guarda la fecha seleccionada."""
        self.fecha_seleccionada = self.calendario.selectedDate().toString("yyyy-MM-dd")
        if self.cancha_seleccionada:
            self.actualizar_horas()

    def seleccionar_cancha(self):
        """Solo una cancha activa (azul); las demás apagadas."""
        boton = self.sender()
        for b in self.botones_cancha:
            if b == boton:
                b.setChecked(True)
                b.setStyleSheet(self.estilo_boton_encendido())
            else:
                b.setChecked(False)
                b.setStyleSheet(self.estilo_boton_apagado())

        self.cancha_seleccionada = next(
            (c for c in self.gestor.canchas if c.nombre == boton.text()), None
        )

        self.label_costo.setText(f"Costo: ${self.cancha_seleccionada.costo:,.0f} COP")

        if self.fecha_seleccionada:
            self.actualizar_horas()

    def actualizar_horas(self):
        """Actualiza lista de horas disponibles."""
        self.lista_horas.clear()
        self.hora_seleccionada = None
        self.boton_confirmar.setEnabled(False)

        if not (self.fecha_seleccionada and self.cancha_seleccionada):
            return

        for hora in [f"{h}:00" for h in range(10, 23)]:
            if self.cancha_seleccionada.disponible(self.fecha_seleccionada, hora):
                self.lista_horas.addItem(f"🟢 {hora} - Disponible")
            else:
                self.lista_horas.addItem(f"🔴 {hora} - Reservada")

    def seleccionar_hora(self, item):
        """Selecciona hora disponible."""
        if "🔴" in item.text():
            QMessageBox.warning(self, "No disponible", "Esa hora ya está reservada.")
            return
        self.hora_seleccionada = item.text().split()[1]
        self.boton_confirmar.setEnabled(True)

    def confirmar_reserva(self):
        """Valida datos del cliente y crea la reserva."""
        if not (self.fecha_seleccionada and self.cancha_seleccionada and self.hora_seleccionada):
            QMessageBox.warning(self, "Incompleto", "Seleccione fecha, cancha y hora primero.")
            return

        nombre, ok1 = QInputDialog.getText(self, "Cliente", "Ingrese nombre y apellido:")
        if not ok1 or not nombre.strip():
            return
        partes = nombre.strip().split()
        if len(partes) < 2:
            QMessageBox.warning(self, "Inválido", "Debe ingresar al menos un nombre y un apellido.")
            return

        telefono, ok2 = QInputDialog.getText(self, "Teléfono", "Ingrese el teléfono (solo números):")
        if not ok2 or not telefono.strip() or not telefono.isdigit() or len(telefono) < 10:
            QMessageBox.warning(self, "Inválido", "El teléfono solo debe contener números y minimo 10 digitos.")
            return

        cliente = Cliente(nombre.strip(), telefono)

        try:
            self.gestor.agregar_reserva(cliente, self.cancha_seleccionada,
                                        self.fecha_seleccionada, self.hora_seleccionada)
            QMessageBox.information(
                self, "Éxito",
                f"Reserva confirmada:\n\n{self.cancha_seleccionada.nombre}\n"
                f"{self.fecha_seleccionada} - {self.hora_seleccionada}\n"
                f"Cliente: {cliente.nombre}"
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
