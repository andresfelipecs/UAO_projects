import json
from clases.reserva import Reserva
from clases.cliente import Cliente
from clases.cancha import Cancha

class GestorReservas:
    def __init__(self, archivo="data.json"):
        self.archivo = archivo
        self.reservas = []
        self.canchas = [
            Cancha("Cancha Sintética", "Fútbol 5", 40000),
            Cancha("Cancha Vóley Playa", "Vóley", 30000),
        ]
        self.cargar_datos()

    def agregar_reserva(self, cliente, cancha, hora):
        if not cancha.disponible(hora):
            raise ValueError("Esa hora ya está reservada.")
        reserva = Reserva(cliente, cancha, hora)
        cancha.reservas.append(reserva)
        self.reservas.append(reserva)
        self.guardar_datos()

    def eliminar_reserva(self, indice):
        del self.reservas[indice]
        self.guardar_datos()

    def guardar_datos(self):
        data = [
            {
                "cliente": r.cliente.nombre,
                "telefono": r.cliente.telefono,
                "cancha": r.cancha.nombre,
                "hora": r.hora
            }
            for r in self.reservas
        ]
        with open(self.archivo, "w") as f:
            json.dump(data, f, indent=4)

    def cargar_datos(self):
        try:
            with open(self.archivo, "r") as f:
                data = json.load(f)
                for d in data:
                    cancha = next(c for c in self.canchas if c.nombre == d["cancha"])
                    cliente = Cliente(d["cliente"], d["telefono"])
                    self.reservas.append(Reserva(cliente, cancha, d["hora"]))
        except FileNotFoundError:
            pass
