class DispositivoElectronico:
    """
    Clase base para todos los dispositivos electrónicos.
    """

    def __init__(self, marca: str, modelo: str, precio: float):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.estado = "Disponible"

    def mostrar_informacion(self) -> str:
        return f"{self.marca} {self.modelo} - ${self.precio:.2f} - Estado: {self.estado}"


class Smartphone(DispositivoElectronico):
    def __init__(self, marca, modelo, precio, sistema, camara):
        super().__init__(marca, modelo, precio)
        self.sistema = sistema
        self.camara = camara

    def mostrar_informacion(self) -> str:
        return super().mostrar_informacion() + f" | SO: {self.sistema}, Cámara: {self.camara}MP"


class Tablet(DispositivoElectronico):
    def __init__(self, marca, modelo, precio, pantalla, bateria):
        super().__init__(marca, modelo, precio)
        self.pantalla = pantalla
        self.bateria = bateria

    def mostrar_informacion(self) -> str:
        return super().mostrar_informacion() + f" | Pantalla: {self.pantalla}'', Batería: {self.bateria}mAh"


class Portatil(DispositivoElectronico):
    def __init__(self, marca, modelo, precio, procesador, ram):
        super().__init__(marca, modelo, precio)
        self.procesador = procesador
        self.ram = ram

    def mostrar_informacion(self) -> str:
        return super().mostrar_informacion() + f" | CPU: {self.procesador}, RAM: {self.ram}GB"
