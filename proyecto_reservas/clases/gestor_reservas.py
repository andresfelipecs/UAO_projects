import json
from clases.reserva import Reserva
from clases.cliente import Cliente
from clases.cancha import Cancha


class GestorReservas:
    """
    Clase encargada de gestionar todas las reservas y la persistencia de datos.
    """

    def __init__(self, archivo="data.json"):
        self.archivo = archivo
        self.reservas = []
        self.canchas = [
            Cancha("Cancha Sintética", "Fútbol 5", 40000),
            Cancha("Cancha Vóley Playa", "Vóley", 30000),
            Cancha("Cancha Techada", "Baloncesto", 35000),
        ]
        self.cargar_datos()

    # ======================================
    #      MÉTODOS PRINCIPALES
    # ======================================

    def agregar_reserva(self, cliente, cancha, fecha, hora):
        """
        Agrega una nueva reserva si la cancha está disponible.
        """
        if not cancha.disponible(fecha, hora):
            raise ValueError("❌ Esa cancha ya está reservada a esa hora.")

        reserva = Reserva(cliente, cancha, fecha, hora)
        cancha.reservar(fecha, hora)
        self.reservas.append(reserva)
        self.guardar_datos()

    def eliminar_reserva(self, indice):
        """
        Elimina la reserva en la posición indicada.
        """
        if 0 <= indice < len(self.reservas):
            reserva = self.reservas[indice]
            reserva.cancha.cancelar_reserva(reserva.fecha, reserva.hora)
            del self.reservas[indice]
            self.guardar_datos()

    # ======================================
    #        PERSISTENCIA DE DATOS
    # ======================================

    def guardar_datos(self):
        """
        Guarda las reservas en el archivo JSON con toda la información relevante.
        """
        data = [
            {
                "cliente": r.cliente.nombre,
                "telefono": r.cliente.telefono,
                "cancha": r.cancha.nombre,
                "fecha": r.fecha,
                "hora": r.hora,
                "costo": r.costo
            }
            for r in self.reservas
        ]

        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def cargar_datos(self):
        """
        Carga las reservas desde el archivo JSON.
        Es tolerante con archivos antiguos (sin fecha o costo).
        """
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                for d in data:
                    cancha = next((c for c in self.canchas if c.nombre == d["cancha"]), None)
                    if cancha:
                        cliente = Cliente(d["cliente"], d["telefono"])

                        # Compatibilidad con versiones anteriores
                        fecha = d.get("fecha", "2025-10-08")
                        hora = d.get("hora", "10:00")
                        costo = d.get("costo", cancha.costo)

                        cancha.reservar(fecha, hora)
                        reserva = Reserva(cliente, cancha, fecha, hora)
                        reserva.costo = costo
                        self.reservas.append(reserva)
        except FileNotFoundError:
            # Si no existe el archivo, lo crea vacío
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
        except json.JSONDecodeError:
            # Si el archivo está corrupto o vacío, lo reinicia
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    # ======================================
    #          FUNCIONES EXTRA
    # ======================================

    def obtener_ingresos_totales(self):
        """
        Retorna la suma total de todos los ingresos generados.
        """
        return sum(r.costo for r in self.reservas)

    def obtener_reservas_por_fecha(self, fecha):
        """
        Retorna las reservas de una fecha específica.
        """
        return [r for r in self.reservas if r.fecha == fecha]

    def obtener_disponibilidad_por_fecha(self, fecha):
        """
        Retorna la disponibilidad de todas las canchas en una fecha.
        """
        disponibilidad = {}
        for cancha in self.canchas:
            horas_libres = []
            for h in [f"{x}:00" for x in range(10, 23)]:
                if cancha.disponible(fecha, h):
                    horas_libres.append(h)
            disponibilidad[cancha.nombre] = horas_libres
        return disponibilidad
