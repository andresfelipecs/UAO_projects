class Estudiante:
    def __init__(self, nombre, apellidos, nota1, nota2, nota3):
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__nota1 = nota1
        self.__nota2 = nota2
        self.__nota3 = nota3

    def get_nombre(self):
        return self.__nombre

    def get_apellidos(self):
        return self.__apellidos

    def get_nota1(self):
        return self.__nota1

    def get_nota2(self):
        return self.__nota2

    def get_nota3(self):
        return self.__nota3

    def set_nota1(self, nota):
        self.__nota1 = nota

    def set_nota2(self, nota):
        self.__nota2 = nota

    def set_nota3(self, nota):
        self.__nota3 = nota

    def calcular_definitiva(self):
        return round((self.__nota1 + self.__nota2 + self.__nota3) / 3, 2)

    def aprobo(self):
        return self.calcular_definitiva() >= 3.0

    def mostrar_info(self):
        estado = "Aprobó" if self.aprobo() else "Reprobó"
        return f"{self.__nombre} {self.__apellidos} - Definitiva: {self.calcular_definitiva()} - {estado}"


# -------------------------------
# Programa principal
# -------------------------------

def main():
    estudiantes = []

    n = int(input("¿Cuántos estudiantes desea ingresar? "))

    for i in range(n):
        print(f"\nEstudiante {i+1}")
        nombre = input("Nombre: ")
        apellidos = input("Apellidos: ")
        nota1 = float(input("Nota 1: "))
        nota2 = float(input("Nota 2: "))
        nota3 = float(input("Nota 3: "))

        estudiante = Estudiante(nombre, apellidos, nota1, nota2, nota3)
        estudiantes.append(estudiante)

    print("\n--- Resultados ---")
    for est in estudiantes:
        print(est.mostrar_info())


if __name__ == "__main__":
    main()
