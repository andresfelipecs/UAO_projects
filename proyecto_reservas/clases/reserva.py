class Reserva:
    def __init__(self, cliente, cancha, fecha, hora):
        self.cliente = cliente
        self.cancha = cancha
        self.fecha = fecha
        self.hora = hora
        self.costo = cancha.costo

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.cliente.nombre} - {self.cancha.nombre} - ${self.costo:,.0f}"
