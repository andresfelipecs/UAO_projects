# biblioteca.py
"""Clase Biblioteca: gestiona libros, usuarios y préstamos."""
from typing import Dict, List
from datetime import date

from libro import Libro
from usuario import Usuario
from prestamo import Prestamo

class Biblioteca:
    def __init__(self) -> None:
        self.libros: Dict[str, Libro] = {}
        self.usuarios: Dict[str, Usuario] = {}
        self.prestamos: List[Prestamo] = []

    def add_book(self, libro: Libro) -> None:
        if libro.codigo in self.libros:
            raise ValueError(f"El código {libro.codigo} ya existe en la biblioteca.")
        self.libros[libro.codigo] = libro

    def add_user(self, usuario: Usuario) -> None:
        if usuario.identificador in self.usuarios:
            raise ValueError(f"El identificador {usuario.identificador} ya existe.")
        self.usuarios[usuario.identificador] = usuario

    def list_all_books(self) -> List[Libro]:
        return list(self.libros.values())

    def list_available_books(self) -> List[Libro]:
        return [l for l in self.libros.values() if l.disponibles > 0]

    def search_by_title(self, termino: str) -> List[Libro]:
        term = termino.lower()
        return [l for l in self.libros.values() if term in l.titulo.lower()]

    def search_by_author(self, termino: str) -> List[Libro]:
        term = termino.lower()
        return [l for l in self.libros.values() if term in l.autor.lower()]

    def search_by_area(self, termino: str) -> List[Libro]:
        term = termino.lower()
        return [l for l in self.libros.values() if term in l.area.lower()]

    def user_loans(self, user_id: str) -> List[Prestamo]:
        return [p for p in self.prestamos if p.usuario.identificador == user_id]

    def lend_book(self, user_id: str, book_code: str, dias_prestamo: int = None) -> Prestamo:
        if user_id not in self.usuarios:
            raise ValueError("Usuario no encontrado.")
        if book_code not in self.libros:
            raise ValueError("Libro no encontrado.")

        usuario = self.usuarios[user_id]
        libro = self.libros[book_code]

        if libro.disponibles <= 0:
            raise ValueError("No hay unidades disponibles para préstamo.")

        prestamos_usuario = self.user_loans(user_id)
        if len(prestamos_usuario) >= 3:
            raise ValueError("El usuario ya tiene 3 préstamos activos.")

        if dias_prestamo is None:
            dias_prestamo = 14 if usuario.tipo == "estudiante" else 30

        fecha = date.today()
        prestamo = Prestamo(usuario=usuario, libro=libro, fecha_prestamo=fecha, dias_prestamo=dias_prestamo)

        libro.prestar()
        self.prestamos.append(prestamo)
        return prestamo

    def return_book(self, user_id: str, book_code: str) -> dict:
        encontrado = None
        for p in self.prestamos:
            if p.usuario.identificador == user_id and p.libro.codigo == book_code:
                encontrado = p
                break

        if encontrado is None:
            raise ValueError("No existe un préstamo activo con ese usuario y libro.")

        hoy = date.today()
        vencido = encontrado.esta_vencido(hoy)
        dias_mora = encontrado.dias_de_mora(hoy)

        encontrado.libro.devolver()
        self.prestamos.remove(encontrado)

        return {"vencido": vencido, "dias_mora": dias_mora, "prestamo": encontrado}

    def get_all_loans(self) -> List[Prestamo]:
        return list(self.prestamos)
