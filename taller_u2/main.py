# main.py
"""Script de interacción para la Biblioteca (CLI simple)."""
from datetime import date
from biblioteca import Biblioteca
from libro import Libro
from usuario import Usuario

def populate_sample_data(bib: Biblioteca) -> None:
    libros = [
        Libro(codigo="B001", titulo="Introducción a Python", autor="Guido van Rossum", anio_publicacion=2010, area="Programación", unidades=4),
        Libro(codigo="B002", titulo="Estructuras de Datos", autor="Niklaus Wirth", anio_publicacion=1985, area="Programación", unidades=3),
        Libro(codigo="B003", titulo="Física Universitaria", autor="Young & Freedman", anio_publicacion=2012, area="Física", unidades=2),
        Libro(codigo="B004", titulo="Cálculo", autor="James Stewart", anio_publicacion=2007, area="Matemáticas", unidades=5),
        Libro(codigo="B005", titulo="Historia de Colombia", autor="Laura Restrepo", anio_publicacion=2015, area="Historia", unidades=2),
        Libro(codigo="B006", titulo="Literatura Moderna", autor="Gabriel García Márquez", anio_publicacion=1990, area="Literatura", unidades=3),
        Libro(codigo="B007", titulo="Química General", autor="Brady", anio_publicacion=2009, area="Química", unidades=2),
        Libro(codigo="B008", titulo="Biología Celular", autor="Alberts", anio_publicacion=2014, area="Biología", unidades=1),
        Libro(codigo="B009", titulo="Economía Básica", autor="Paul Krugman", anio_publicacion=2011, area="Economía", unidades=2),
        Libro(codigo="B010", titulo="Diseño de Sistemas", autor="Andrew Tanenbaum", anio_publicacion=2005, area="Ingeniería", unidades=3),
    ]

    for l in libros:
        bib.add_book(l)

    usuarios = [
        Usuario(nombre="Carlos Alberto Dorado Vega", identificador="U001", tipo="estudiante"),
        Usuario(nombre="María López", identificador="U002", tipo="profesor"),
        Usuario(nombre="Juan Pérez", identificador="U003", tipo="estudiante"),
    ]

    for u in usuarios:
        bib.add_user(u)

def print_books(libros):
    if not libros:
        print("No se encontraron libros.")
        return
    for l in libros:
        print(l)

def run_cli():
    bib = Biblioteca()
    populate_sample_data(bib)

    menu = ("\n=== MENÚ BIBLIOTECA ===\n"
            "1. Listar todos los libros\n"
            "2. Listar libros disponibles\n"
            "3. Buscar libros por título\n"
            "4. Buscar libros por autor\n"
            "5. Buscar libros por área\n"
            "6. Realizar préstamo\n"
            "7. Devolver libro\n"
            "8. Consultar préstamos por usuario\n"
            "9. Ver todos los préstamos activos\n"
            "0. Salir\n"
            "Elija una opción: ")

    while True:
        opcion = input(menu).strip()
        try:
            if opcion == "1":
                print_books(bib.list_all_books())
            elif opcion == "2":
                print_books(bib.list_available_books())
            elif opcion == "3":
                termino = input("Ingrese término de búsqueda (título): ").strip()
                print_books(bib.search_by_title(termino))
            elif opcion == "4":
                termino = input("Ingrese término de búsqueda (autor): ").strip()
                print_books(bib.search_by_author(termino))
            elif opcion == "5":
                termino = input("Ingrese término de búsqueda (área): ").strip()
                print_books(bib.search_by_area(termino))
            elif opcion == "6":
                user_id = input("Identificador del usuario: ").strip()
                book_code = input("Código del libro: ").strip()
                dias = input("Días de préstamo (ENTER para usar el valor por defecto según tipo de usuario): ").strip()
                dias_val = int(dias) if dias else None
                prestamo = bib.lend_book(user_id, book_code, dias_val)
                print(f"Préstamo realizado con éxito: {prestamo}")
            elif opcion == "7":
                user_id = input("Identificador del usuario: ").strip()
                book_code = input("Código del libro: ").strip()
                resultado = bib.return_book(user_id, book_code)
                if resultado["vencido"]:
                    print(f"Devolución registrada. El libro está vencido. Días de mora: {resultado['dias_mora']}")
                else:
                    print("Devolución registrada a tiempo. Gracias.")
            elif opcion == "8":
                user_id = input("Identificador del usuario: ").strip()
                prestamos = bib.user_loans(user_id)
                if not prestamos:
                    print("El usuario no tiene préstamos activos.")
                else:
                    for p in prestamos:
                        estado = "VENCIDO" if p.esta_vencido() else "EN TIEMPO"
                        print(f"{p} -> Estado: {estado} | Días de mora: {p.dias_de_mora()}")
            elif opcion == "9":
                prestamos = bib.get_all_loans()
                if not prestamos:
                    print("No hay préstamos activos.")
                else:
                    for p in prestamos:
                        print(p)
            elif opcion == "0":
                print("Saliendo. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_cli()
