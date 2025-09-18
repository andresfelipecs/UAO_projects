
class Rectangulo:
    def __init__(self, base, altura):
        self.base = base        
        self.altura = altura   

    def mostrar_todo(self):
        return f"Base: {self.base} cm, Altura: {self.altura} cm"

    def calcular_area(self):
        return self.base * self.altura

    def calcular_perimetro(self):
        return 2 * (self.base + self.altura)


if __name__ == "__main__":
    
    rect1 = Rectangulo(10, 5)
    rect2 = Rectangulo(8, 12)
    rect3 = Rectangulo(15, 7)

    rectangulos = [rect1, rect2, rect3]

    for i, rect in enumerate(rectangulos, start=1):
        print(f"\nRectángulo {i}:")
        print(rect.mostrar_todo())
        print(f"Área: {rect.calcular_area()} cm²")
        print(f"Perímetro: {rect.calcular_perimetro()} cm")
