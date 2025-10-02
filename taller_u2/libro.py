# libro.py
"""
Curso: Programación G02
Docente: Breyner Posso M.Sc. 
Integrantes:
Jose Alberto Ortiz Valencia
Carlos Aberto Dorado Vega
Andres Felipe Castro Salazar
Brayan Gutierrez Rengifo
"""
from dataclasses import dataclass

@dataclass
class Libro:
    codigo: str
    titulo: str
    autor: str
    anio_publicacion: int
    area: str
    unidades: int
    disponibles: int = None

    def __post_init__(self):
        if self.disponibles is None:
            self.disponibles = int(self.unidades)

    def prestar(self) -> None:
        """Reduce en 1 las unidades disponibles. Lanza ValueError si no hay disponibles."""
        if self.disponibles <= 0:
            raise ValueError(f"No hay unidades disponibles del libro '{self.titulo}' (código {self.codigo}).")
        self.disponibles -= 1

    def devolver(self) -> None:
        """Aumenta en 1 las unidades disponibles. Lanza ValueError si excede el total de unidades."""
        if self.disponibles >= self.unidades:
            raise ValueError("No se pueden devolver más unidades que las existentes.")
        self.disponibles += 1

    def __str__(self) -> str:
        return (f"{self.codigo} | {self.titulo} - {self.autor} ({self.anio_publicacion}) " +
                f"[{self.area}] Unidades: {self.unidades} Disponibles: {self.disponibles}")
