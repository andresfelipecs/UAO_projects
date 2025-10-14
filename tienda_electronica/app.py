from clases import Smartphone, Tablet, Portatil

#Integrantes:
# Jose Alberto Ortiz Valencia
# Carlos Aberto Dorado Vega
# Andres Felipe Castro Salazar
# Brayan Gutierrez Rengifo

# Inventario de la tienda
inventario = [
    Smartphone("Apple", "iPhone 15", 6_500_000, "iOS", 48),
    Smartphone("Samsung", "Galaxy S23", 4_500_000, "Android", 50),
    Tablet("Apple", "iPad Pro", 5_800_000, 12.9, 10758),
    Tablet("Samsung", "Galaxy Tab S9", 3_800_000, 11, 8000),
    Portatil("Dell", "XPS 13", 7_200_000, "Intel i7", 16),
    Portatil("Lenovo", "ThinkPad X1", 8_500_000, "Intel i9", 32),
]


def pedir_float(mensaje):
    """Solicita un número flotante validado"""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número decimal (ej: 1499.99).")


def pedir_int(mensaje):
    """Solicita un número entero validado"""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número entero (ej: 8).")


def agregar_dispositivo():
    print("\n1. Smartphone\n2. Tablet\n3. Portátil")
    tipo = input("Seleccione el tipo de dispositivo: ")

    marca = input("Marca: ")
    modelo = input("Modelo: ")
    precio = pedir_float("Precio: ")

    if tipo == "1":
        sistema = input("Sistema Operativo: ")
        camara = pedir_int("Cámara (MP): ")
        dispositivo = Smartphone(marca, modelo, precio, sistema, camara)

    elif tipo == "2":
        pantalla = pedir_float("Tamaño pantalla (pulgadas): ")
        bateria = pedir_int("Batería (mAh): ")
        dispositivo = Tablet(marca, modelo, precio, pantalla, bateria)

    elif tipo == "3":
        procesador = input("Procesador: ")
        ram = pedir_int("RAM (GB): ")
        dispositivo = Portatil(marca, modelo, precio, procesador, ram)

    else:
        print("❌ Opción no válida. Debe ser 1, 2 o 3.")
        return

    inventario.append(dispositivo)
    print("✅ Dispositivo agregado al inventario.")


def listar_dispositivos():
    if not inventario:
        print("\n📭 Inventario vacío.")
        return

    print("\n📋 Inventario de la tienda:")
    for i, d in enumerate(inventario, start=1):
        print(f"{i}. {d.mostrar_informacion()}")


def vender_dispositivo():
    if not inventario:
        print("\n📭 No hay dispositivos para vender.")
        return

    listar_dispositivos()
    try:
        idx = int(input("Seleccione el número del dispositivo a vender: ")) - 1
        if 0 <= idx < len(inventario):
            print("\n1. Marcar como vendido")
            print("2. Eliminar del inventario")
            opcion = input("Seleccione: ")

            if opcion == "1":
                inventario[idx].estado = "Vendido"
                print("💰 Dispositivo marcado como vendido.")
            elif opcion == "2":
                vendido = inventario.pop(idx)
                print(f"🗑️ Dispositivo '{vendido.marca} {vendido.modelo}' eliminado del inventario.")
            else:
                print("❌ Opción no válida.")
        else:
            print("❌ Número inválido.")
    except ValueError:
        print("❌ Entrada inválida. Debe ser un número entero.")


def gestionar_devoluciones():
    """Permite devolver un dispositivo vendido (lo pasa a 'Disponible')."""
    if not inventario:
        print("\n📭 No hay dispositivos para devolver.")
        return

    listar_dispositivos()
    try:
        idx = int(input("Seleccione el número del dispositivo a devolver: ")) - 1
        if 0 <= idx < len(inventario):
            if inventario[idx].estado == "Vendido":
                inventario[idx].estado = "Disponible"
                print("🔄 Dispositivo devuelto y disponible nuevamente.")
            else:
                print("❌ Solo se pueden devolver dispositivos vendidos.")
        else:
            print("❌ Número inválido.")
    except ValueError:
        print("❌ Entrada inválida. Debe ser un número entero.")


def ingresar_reparacion():
    """Marca un dispositivo como 'En reparación'."""
    if not inventario:
        print("\n📭 No hay dispositivos para reparar.")
        return

    listar_dispositivos()
    try:
        idx = int(input("Seleccione el número del dispositivo a reparar: ")) - 1
        if 0 <= idx < len(inventario):
            inventario[idx].estado = "En reparación"
            print("🛠️ Dispositivo ingresado a reparación.")
        else:
            print("❌ Número inválido.")
    except ValueError:
        print("❌ Entrada inválida. Debe ser un número entero.")


def buscar_dispositivo():
    """Busca un dispositivo por marca o modelo."""
    if not inventario:
        print("\n📭 No hay dispositivos para buscar.")
        return

    criterio = input("Ingrese marca o modelo a buscar: ").lower()
    resultados = [d for d in inventario if criterio in d.marca.lower() or criterio in d.modelo.lower()]

    if resultados:
        print("\n🔎 Resultados de la búsqueda:")
        for d in resultados:
            print(d.mostrar_informacion())
    else:
        print("❌ No se encontraron coincidencias.")


def menu():
    while True:
        print("\n--- Tienda Electrónica ---")
        print("1. Ingresar dispositivo")
        print("2. Listar dispositivos")
        print("3. Vender dispositivo")
        print("4. Gestionar devoluciones")
        print("5. Ingresar a reparación")
        print("6. Buscar dispositivo")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_dispositivo()
        elif opcion == "2":
            listar_dispositivos()
        elif opcion == "3":
            vender_dispositivo()
        elif opcion == "4":
            gestionar_devoluciones()
        elif opcion == "5":
            ingresar_reparacion()
        elif opcion == "6":
            buscar_dispositivo()
        elif opcion == "7":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida. Ingrese un número del 1 al 7.")


if __name__ == "__main__":
    menu()
