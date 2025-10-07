class Cancha:
    def __init__(self, nombre, tipo, costo):
        self.nombre = nombre
        self.tipo = tipo
        self.costo = costo
        self.reservas = []  # lista de objetos Reserva

    def disponible(self, hora):
        """
        Verifica si la cancha está libre a una hora dada.
        Retorna True si no hay reservas en esa hora.
        """
        for reserva in self.reservas:
            if reserva.hora == hora:
                return False
        return True

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - ${self.costo:,.0f} COP"
