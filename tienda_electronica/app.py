from clases import Smartphone, Tablet, Portatil

# Inventario de la tienda
inventario = []

def agregar_dispositivo():
    print("\n1. Smartphone\n2. Tablet\n3. Portátil")
    tipo = input("Seleccione el tipo de dispositivo: ")

    marca = input("Marca: ")
    modelo = input("Modelo: ")
    precio = float(input("Precio: "))

    if tipo == "1":
        sistema = input("Sistema Operativo: ")
        camara = int(input("Cámara (MP): "))
        dispositivo = Smartphone(marca, modelo, precio, sistema, camara)

    elif tipo == "2":
        pantalla = float(input("Tamaño pantalla (pulgadas): "))
        bateria = int(input("Batería (mAh): "))
        dispositivo = Tablet(marca, modelo, precio, pantalla, bateria)

    elif tipo == "3":
        procesador = input("Procesador: ")
        ram = int(input("RAM (GB): "))
        dispositivo = Portatil(marca, modelo, precio, procesador, ram)

    else:
        print("Opción no válida")
        return

    inventario.append(dispositivo)
    print("✅ Dispositivo agregado al inventario.")


def listar_dispositivos():
    print("\n📋 Inventario de la tienda:")
    for i, d in enumerate(inventario, start=1):
        print(f"{i}. {d.mostrar_informacion()}")


def vender_dispositivo():
    listar_dispositivos()
    idx = int(input("Seleccione el número del dispositivo a vender: ")) - 1
    if 0 <= idx < len(inventario):
        inventario[idx].estado = "Vendido"
        print("💰 Dispositivo vendido con éxito.")
    else:
        print("❌ Selección inválida.")


def menu():
    while True:
        print("\n--- Tienda Electrónica ---")
        print("1. Ingresar dispositivo")
        print("2. Listar dispositivos")
        print("3. Vender dispositivo")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_dispositivo()
        elif opcion == "2":
            listar_dispositivos()
        elif opcion == "3":
            vender_dispositivo()
        elif opcion == "4":
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    menu()
