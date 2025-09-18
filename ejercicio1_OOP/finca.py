class Finca:
    def __init__(self, base_metros, altura_metros, precio_por_hectarea):
        self.base = base_metros
        self.altura = altura_metros
        self.precio = precio_por_hectarea

    def calcular_area_hectareas(self):
        area_m2 = self.base * self.altura
        return area_m2 / 10000   

    def calcular_costo_total(self):
        return self.calcular_area_hectareas() * self.precio

    def mostrar_info(self):
        return (f"Dimensiones: {self.base}m x {self.altura}m | "
                f"Área: {self.calcular_area_hectareas():.2f} ha | "
                f"Costo total: ${self.calcular_costo_total():,.2f}")



if __name__ == "__main__":
    finca1 = Finca(200, 300, 5000000)   
    finca2 = Finca(500, 400, 4500000)
    finca3 = Finca(1000, 800, 6000000)

    fincas = [finca1, finca2, finca3]

    for i, finca in enumerate(fincas, 1):
        print(f"\nFinca {i}:")
        print(finca.mostrar_info())
