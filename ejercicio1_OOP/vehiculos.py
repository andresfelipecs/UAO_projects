
class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def descripcion(self):
        return f"Vehículo {self.marca} {self.modelo}"

    def mover(self):
        return "El vehículo se mueve."


class Coche(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)
        self.puertas = puertas


    def mover(self):
        return f"El coche {self.marca} avanza por la carretera."

    def tocar_bocina(self, veces=1):
        return "¡Beep! " * veces


class Bicicleta(Vehiculo):
    def __init__(self, marca, modelo, tipo):
        super().__init__(marca, modelo)
        self.tipo = tipo

    def mover(self):
        return f"La bicicleta {self.marca} pedalea por el carril bici."


vehiculos = [
    Coche("Toyota", "Corolla", 4),         
    Bicicleta("Trek", "FX 3", "montaña"), 
    Vehiculo("Genérico", "2025")        
]

for v in vehiculos:
    print(v.descripcion())  
    print(v.mover())         


c = Coche("Mazda", "3", 4)
print(c.tocar_bocina())   
print(c.tocar_bocina(3))    
