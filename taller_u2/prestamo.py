# prestamo.py
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
from datetime import date, timedelta
from typing import Optional

from usuario import Usuario
from libro import Libro

@dataclass
class Prestamo:
    usuario: Usuario
    libro: Libro
    fecha_prestamo: date
    dias_prestamo: int
    fecha_devolucion: Optional[date] = None

    def __post_init__(self):
        if self.fecha_devolucion is None:
            self.fecha_devolucion = self.fecha_prestamo + timedelta(days=self.dias_prestamo)

    def esta_vencido(self, fecha_actual: Optional[date] = None) -> bool:
        if fecha_actual is None:
            fecha_actual = date.today()
        return fecha_actual > self.fecha_devolucion

    def dias_de_mora(self, fecha_actual: Optional[date] = None) -> int:
        if fecha_actual is None:
            fecha_actual = date.today()
        delta = fecha_actual - self.fecha_devolucion
        return max(0, delta.days)

    def __str__(self) -> str:
        return (f"{self.libro.codigo} | '{self.libro.titulo}' -> {self.usuario.nombre} " +
                f"(desde {self.fecha_prestamo.isoformat()} hasta {self.fecha_devolucion.isoformat()})")
