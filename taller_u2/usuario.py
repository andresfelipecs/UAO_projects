# usuario.py
"""Clase Usuario para el sistema de biblioteca."""
from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    identificador: str
    tipo: str  # 'estudiante' o 'profesor'

    def __post_init__(self):
        tipo_lower = self.tipo.lower()
        if tipo_lower not in ("estudiante", "profesor"):
            raise ValueError("El tipo de usuario debe ser 'estudiante' o 'profesor'.")
        self.tipo = tipo_lower

    def __str__(self) -> str:
        return f"{self.identificador} | {self.nombre} ({self.tipo})"
