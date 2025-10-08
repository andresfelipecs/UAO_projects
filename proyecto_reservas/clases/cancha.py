from datetime import date

class Cancha:
    def __init__(self, nombre, tipo, costo):
        self.nombre = nombre
        self.tipo = tipo
        self.costo = costo
        # Diccionario de reservas: {"2025-10-07": ["10:00", "11:00"]}
        self.reservas_por_dia = {}

    def disponible(self, fecha: str, hora: str):
        """Verifica si la cancha está libre a una fecha y hora."""
        if fecha not in self.reservas_por_dia:
            return True
        return hora not in self.reservas_por_dia[fecha]

    def reservar(self, fecha: str, hora: str):
        """Marca la cancha como reservada para esa fecha y hora."""
        if fecha not in self.reservas_por_dia:
            self.reservas_por_dia[fecha] = []
        self.reservas_por_dia[fecha].append(hora)

    def cancelar_reserva(self, fecha: str, hora: str):
        if fecha in self.reservas_por_dia and hora in self.reservas_por_dia[fecha]:
            self.reservas_por_dia[fecha].remove(hora)

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - ${self.costo:,.0f} COP"
