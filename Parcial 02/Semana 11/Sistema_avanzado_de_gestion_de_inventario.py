# 📦 SISTEMA AVANZADO DE GESTIÓN DE INVENTARIO

import json
import os
from typing import Dict, List, Set
from collections import defaultdict

# ===============================
# 📦 Clase Producto
# ===============================
class Producto:
    def __init__(self, id: str, nombre: str, cantidad: int, precio: float):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        if not value.strip():
            raise ValueError("El ID no puede estar vacío.")
        self._id = value.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = value.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value: int):
        if value < 0:
            raise ValueError("La cantidad debe ser mayor o igual a cero.")
        self._cantidad = value

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, value: float):
        if value < 0:
            raise ValueError("El precio debe ser mayor o igual a cero.")
        self._precio = round(value, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data: Dict):
        return Producto(data["id"], data["nombre"], data["cantidad"], data["precio"])

    def __str__(self):
        return f"{self.id:<8} | {self.nombre:<20} | {self.cantidad:<8} | ${self.precio:<8.2f}"

# ===============================
# 📁 Clase Inventario
# ===============================
class Inventario:
    ARCHIVO = "inventario.json"

    def __init__(self):
        self._productos: Dict[str, Producto] = {}
        self._indice_nombre: defaultdict[str, Set[str]] = defaultdict(set)
        self.cargar()

    def agregar(self, producto: Producto):
        if producto.id in self._productos:
            raise KeyError("ID duplicado.")
        self._productos[producto.id] = producto
        self._indice_nombre[producto.nombre.lower()].add(producto.id)
        self.guardar()

    def eliminar(self, pid: str):
        if pid not in self._productos:
            raise KeyError("Producto no encontrado.")
        nombre = self._productos[pid].nombre.lower()
        self._indice_nombre[nombre].remove(pid)
        if not self._indice_nombre[nombre]:
            del self._indice_nombre[nombre]
        del self._productos[pid]
        self.guardar()

    def actualizar_cantidad(self, pid: str, nueva: int):
        if pid in self._productos:
            self._productos[pid].cantidad = nueva
            self.guardar()
        else:
            raise KeyError("ID no encontrado.")

    def actualizar_precio(self, pid: str, nuevo: float):
        if pid in self._productos:
            self._productos[pid].precio = nuevo
            self.guardar()
        else:
            raise KeyError("ID no encontrado.")

    def buscar(self, texto: str) -> List[Producto]:
        texto = texto.lower()
        ids_encontrados = set()
        for nombre, ids in self._indice_nombre.items():
            if texto in nombre:
                ids_encontrados.update(ids)
        return [self._productos[pid] for pid in ids_encontrados]

    def todos(self) -> List[Producto]:
        return list(self._productos.values())

    def guardar(self):
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self._productos.values()], f, indent=4, ensure_ascii=False)

    def cargar(self):
        if not os.path.exists(self.ARCHIVO):
            return
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for d in datos:
                    prod = Producto.from_dict(d)
                    self._productos[prod.id] = prod
                    self._indice_nombre[prod.nombre.lower()].add(prod.id)
        except Exception as e:
            print(f"⚠ Error cargando inventario: {e}")

# ===============================
# 🧩 Funciones Auxiliares
# ===============================
def imprimir_tabla(productos: List[Producto]):
    if not productos:
        print("📭 No hay productos para mostrar.")
        return
    print(f"\n{'ID':<8} | {'Nombre':<20} | {'Cantidad':<8} | {'Precio':<8}")
    print("-" * 55)
    for p in productos:
        print(p)

def input_entero(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("❌ Por favor, ingrese un número entero válido.")

def input_flotante(msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("❌ Por favor, ingrese un número decimal válido.")

# ===============================
# 📋 Menú Interactivo
# ===============================
def menu():
    inv = Inventario()

    while True:
        print("\n📋 MENÚ DE INVENTARIO")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar cantidad")
        print("4. Actualizar precio")
        print("5. Buscar producto por nombre")
        print("6. Mostrar todo el inventario")
        print("7. Guardar inventario manualmente")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                pid = input("ID: ").strip()
                nombre = input("Nombre: ").strip()
                cantidad = input_entero("Cantidad: ")
                precio = input_flotante("Precio: ")
                inv.agregar(Producto(pid, nombre, cantidad, precio))
                print("✅ Producto añadido.")

            elif opcion == "2":
                pid = input("ID del producto a eliminar: ").strip()
                inv.eliminar(pid)
                print("✅ Producto eliminado.")

            elif opcion == "3":
                pid = input("ID: ").strip()
                nueva_cant = input_entero("Nueva cantidad: ")
                inv.actualizar_cantidad(pid, nueva_cant)
                print("✅ Cantidad actualizada.")

            elif opcion == "4":
                pid = input("ID: ").strip()
                nuevo_precio = input_flotante("Nuevo precio: ")
                inv.actualizar_precio(pid, nuevo_precio)
                print("✅ Precio actualizado.")

            elif opcion == "5":
                nombre = input("Nombre a buscar: ").strip()
                encontrados = inv.buscar(nombre)
                if encontrados:
                    imprimir_tabla(encontrados)
                else:
                    print("❌ No se encontró ningún producto.")

            elif opcion == "6":
                productos = inv.todos()
                imprimir_tabla(productos)

            elif opcion == "7":
                inv.guardar()
                print("💾 Inventario guardado correctamente.")

            elif opcion == "0":
                inv.guardar()
                print("👋 ¡Hasta luego! Inventario guardado.")
                break

            else:
                print("⚠ Opción inválida. Intente de nuevo.")

        except Exception as e:
            print(f"❌ Error: {e}")

# ===============================
# 🚀 Ejecutar el programa
# ===============================
if __name__ == "__main__":
    menu()
