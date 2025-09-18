
class Gato:
    def __init__(self, nombre, edad, color, raza):
        self.nombre = nombre      
        self.edad = edad          
        self.color = color        
        self.raza = raza          
    
    def maullar(self):
        return f"{self.nombre} dice: ¡Miau!"
    
    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Color: {self.color}, Raza: {self.raza}"


if __name__ == "__main__":
    
    gato1 = Gato("Salomon", 4, "beige y cafe", "Siames")
    gato2 = Gato("Soho", 3, "Gris blanco", "Criollo")
    gato3 = Gato("Zoe", 3, "Naranja negro blanco", "Criollo")
    gato4 = Gato("Darko", 2, "Gris", "Persa")

    print(gato1.mostrar_info())
    print(gato1.maullar())
    print(gato2.mostrar_info())
    print(gato3.mostrar_info())
    print(gato4.nombre)
