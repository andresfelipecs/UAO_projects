class Reserva:
    def __init__(self, cliente, cancha, hora):
        self.cliente = cliente
        self.cancha = cancha
        self.hora = hora

    def __str__(self):
        return f"{self.cliente.nombre} - {self.cancha.nombre} - {self.hora}"
