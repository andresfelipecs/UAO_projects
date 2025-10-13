"""
Sistema para gestionar vehículos de una empresa de alquiler (rent-a-car).

Autor: Andres Felipe Castro Salazar
Fecha: 2025-10-10
"""

from typing import List


class Vehiculo:
    """Superclase Vehiculo."""

    def __init__(self, marca: str, modelo: str, anio: int, tipo: str) -> None:
        self._marca = marca.strip()
        self._modelo = modelo.strip()
        self._anio = int(anio)
        self._tipo = tipo.strip()

    def mostrar_informacion(self) -> str:
        info = (
            f"Marca: {self._marca} | Modelo: {self._modelo} | "
            f"Año: {self._anio} | Tipo: {self._tipo}"
        )
        return info

    def calcular_impuesto(self) -> float:
        base = 50.0
        return float(base)


class VehiculoGasolina(Vehiculo):
    """Subclase para vehículos a gasolina."""

    def __init__(self, marca: str, modelo: str, anio: int, tipo: str, cilindraje: int) -> None:
        super().__init__(marca, modelo, anio, tipo)
        self._cilindraje = int(cilindraje)

    def mostrar_informacion(self) -> str:
        base_info = super().mostrar_informacion()
        return f"{base_info} | Combustible: Gasolina | Cilindraje: {self._cilindraje} cc"

    def calcular_impuesto(self) -> float:
        base = super().calcular_impuesto()
        c = self._cilindraje
        if c < 1000:
            factor = 0.0
        elif 1200 <= c < 1600:
            factor = 0.20
        elif c >= 1600:
            factor = 0.40
        else:
            factor = 0.0
        impuesto = base * (1.0 + factor)
        return round(float(impuesto), 2)


class VehiculoElectrico(Vehiculo):
    """Subclase para vehículos eléctricos."""

    def __init__(self, marca: str, modelo: str, anio: int, tipo: str, autonomia: int) -> None:
        super().__init__(marca, modelo, anio, tipo)
        self._autonomia = int(autonomia)

    def mostrar_informacion(self) -> str:
        base_info = super().mostrar_informacion()
        return f"{base_info} | Combustible: Eléctrico | Autonomía: {self._autonomia} km"

    def calcular_impuesto(self) -> float:
        base = super().calcular_impuesto()
        a = self._autonomia
        if a >= 400:
            descuento = 0.40
        elif 200 <= a < 400:
            descuento = 0.20
        else:
            descuento = 0.10
        impuesto = base * (1.0 - descuento)
        return round(float(impuesto), 2)


# ---------- Vehículos precargados en formato "JSON" ----------

VEHICULOS_INICIALES = [
    {"tipo_clase": "gasolina", "marca": "Toyota", "modelo": "Corolla", "anio": 2018, "tipo": "Sedan", "cilindraje": 1600},
    {"tipo_clase": "gasolina", "marca": "Ford", "modelo": "Fiesta", "anio": 2010, "tipo": "Hatchback", "cilindraje": 1200},
    {"tipo_clase": "gasolina", "marca": "Honda", "modelo": "Civic", "anio": 2005, "tipo": "Sedan", "cilindraje": 1800},
    {"tipo_clase": "gasolina", "marca": "Chevrolet", "modelo": "Spark", "anio": 2014, "tipo": "Hatchback", "cilindraje": 998},
    {"tipo_clase": "gasolina", "marca": "BMW", "modelo": "X5", "anio": 2020, "tipo": "SUV", "cilindraje": 3000},
    {"tipo_clase": "electrico", "marca": "Tesla", "modelo": "Model 3", "anio": 2021, "tipo": "Sedan", "autonomia": 500},
    {"tipo_clase": "electrico", "marca": "Nissan", "modelo": "Leaf", "anio": 2019, "tipo": "Hatchback", "autonomia": 240},
    {"tipo_clase": "electrico", "marca": "Renault", "modelo": "Zoe", "anio": 2018, "tipo": "Hatchback", "autonomia": 300},
    {"tipo_clase": "electrico", "marca": "BMW", "modelo": "i3", "anio": 2017, "tipo": "Hatchback", "autonomia": 170},
    {"tipo_clase": "electrico", "marca": "Hyundai", "modelo": "Kona Electric", "anio": 2022, "tipo": "SUV", "autonomia": 450},
]


def cargar_vehiculos_iniciales() -> List[Vehiculo]:
    """Convierte la lista tipo JSON a objetos reales de las clases."""
    vehiculos: List[Vehiculo] = []
    for v in VEHICULOS_INICIALES:
        if v["tipo_clase"] == "gasolina":
            vehiculos.append(
                VehiculoGasolina(v["marca"], v["modelo"], v["anio"], v["tipo"], v["cilindraje"])
            )
        elif v["tipo_clase"] == "electrico":
            vehiculos.append(
                VehiculoElectrico(v["marca"], v["modelo"], v["anio"], v["tipo"], v["autonomia"])
            )
    return vehiculos


# ---------- Funciones del programa ----------

def mostrar_todos_vehiculos(vehiculos: List[Vehiculo]) -> None:
    if not vehiculos:
        print("\n⚠️  No hay vehículos registrados.\n")
        return
    print("\n🚗 --- Lista de vehículos registrados ---")
    for i, v in enumerate(vehiculos, start=1):
        print(f"\n[{i}] {v.mostrar_informacion()}")
        print(f"   💰 Impuesto a pagar: ${v.calcular_impuesto():.2f} USD")
    print("----------------------------------------\n")


def buscar_por_marca(vehiculos: List[Vehiculo], marca: str) -> None:
    marca_q = marca.strip().lower()
    encontrados = [v for v in vehiculos if v._marca.lower() == marca_q]
    if not encontrados:
        print(f"\n❌ No se encontraron vehículos de la marca '{marca}'.\n")
        return
    print(f"\n🔎 Resultados de búsqueda por marca: '{marca}'")
    for v in encontrados:
        tipo_comb = "Gasolina" if isinstance(v, VehiculoGasolina) else "Eléctrico"
        print(f"\n- Tipo de vehículo: {tipo_comb}")
        print(f"  {v.mostrar_informacion()}")
        print(f"  💰 Impuesto: ${v.calcular_impuesto():.2f} USD")
    print("")


def buscar_por_cilindraje(vehiculos: List[Vehiculo], cilindraje: int) -> None:
    encontrados = [
        v for v in vehiculos if isinstance(v, VehiculoGasolina) and v._cilindraje == int(cilindraje)
    ]
    if not encontrados:
        print(f"\n❌ No se encontraron vehículos a gasolina con cilindraje {cilindraje} cc.\n")
        return
    print(f"\n⛽ Vehículos a gasolina con cilindraje {cilindraje} cc:")
    for v in encontrados:
        print(f"  {v.mostrar_informacion()}")
        print(f"   💰 Impuesto: ${v.calcular_impuesto():.2f} USD")
    print("")


def buscar_por_autonomia(vehiculos: List[Vehiculo], autonomia: int) -> None:
    encontrados = [
        v for v in vehiculos
        if isinstance(v, VehiculoElectrico) and v._autonomia >= int(autonomia)
    ]
    if not encontrados:
        print(f"\n❌ No se encontraron vehículos eléctricos con autonomía >= {autonomia} km.\n")
        return
    print(f"\n🔋 Vehículos eléctricos con autonomía >= {autonomia} km:")
    for v in encontrados:
        print(f"  {v.mostrar_informacion()}")
        print(f"   💰 Impuesto: ${v.calcular_impuesto():.2f} USD")
    print("")


def solicitar_entero(prompt: str, minimo: int = None, maximo: int = None) -> int:
    while True:
        entrada = input(prompt).strip()
        if not entrada.isdigit():
            print("  ⚠️  Error: ingresa solo números enteros. Intenta otra vez.")
            continue
        valor = int(entrada)
        if minimo is not None and valor < minimo:
            print(f"  ⚠️  Error: el valor debe ser >= {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"  ⚠️  Error: el valor debe ser <= {maximo}.")
            continue
        return valor


def crear_vehiculo_gasolina() -> VehiculoGasolina:
    print("\n🛠️ Creando vehículo a gasolina:")
    marca = input("  Marca: ").strip()
    modelo = input("  Modelo: ").strip()
    anio = solicitar_entero("  Año (ej. 2023): ", minimo=1886, maximo=2100)
    tipo = input("  Tipo (ej. SUV, Sedan): ").strip()
    cilindraje = solicitar_entero("  Cilindraje (cc): ", minimo=50, maximo=20000)
    vg = VehiculoGasolina(marca, modelo, anio, tipo, cilindraje)
    print("✅ Vehículo a gasolina creado correctamente.\n")
    return vg


def crear_vehiculo_electrico() -> VehiculoElectrico:
    print("\n⚡ Creando vehículo eléctrico:")
    marca = input("  Marca: ").strip()
    modelo = input("  Modelo: ").strip()
    anio = solicitar_entero("  Año (ej. 2023): ", minimo=1886, maximo=2100)
    tipo = input("  Tipo (ej. Hatchback, SUV): ").strip()
    autonomia = solicitar_entero("  Autonomía (km): ", minimo=10, maximo=2000)
    ve = VehiculoElectrico(marca, modelo, anio, tipo, autonomia)
    print("✅ Vehículo eléctrico creado correctamente.\n")
    return ve


def menu_principal() -> None:
    vehiculos: List[Vehiculo] = cargar_vehiculos_iniciales()

    while True:
        print(
            "\n🚙===== MENÚ RENT-A-CAR =====🚙\n"
            "1️⃣  Crear vehículo a gasolina\n"
            "2️⃣  Crear vehículo eléctrico\n"
            "3️⃣  Mostrar todos los vehículos e impuesto\n"
            "4️⃣  Buscar vehículos por marca\n"
            "5️⃣  Buscar vehículos por cilindraje (gasolina)\n"
            "6️⃣  Buscar vehículos por autonomía mínima (eléctrico)\n"
            "7️⃣  Salir 🚪\n"
        )
        opcion = input("👉 Selecciona una opción (1-7): ").strip()

        if opcion == "1":
            vehiculos.append(crear_vehiculo_gasolina())
        elif opcion == "2":
            vehiculos.append(crear_vehiculo_electrico())
        elif opcion == "3":
            mostrar_todos_vehiculos(vehiculos)
        elif opcion == "4":
            marca = input("🔍 Ingresa la marca a buscar: ").strip()
            if marca:
                buscar_por_marca(vehiculos, marca)
            else:
                print("⚠️  Marca vacía. Intenta de nuevo.")
        elif opcion == "5":
            cil = solicitar_entero("🔧 Ingresa el cilindraje exacto (cc): ", minimo=0, maximo=20000)
            buscar_por_cilindraje(vehiculos, cil)
        elif opcion == "6":
            aut = solicitar_entero("🔋 Ingresa autonomía mínima (km): ", minimo=0, maximo=5000)
            buscar_por_autonomia(vehiculos, aut)
        elif opcion == "7":
            print("👋 Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intenta otra vez.")


def main() -> None:
    print("🌟 Sistema de gestión de vehículos - Rent-a-Car 🌟")
    menu_principal()


if __name__ == "__main__":
    main()
