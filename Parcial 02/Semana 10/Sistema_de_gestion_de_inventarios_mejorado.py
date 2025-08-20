# 📦 SISTEMA DE GESTIÓN DE INVENTARIO MEJORADO

import json
import os

class Producto:
    """Representa un producto individual en el inventario."""

    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        return Producto(
            data["id"],
            data["nombre"],
            int(data["cantidad"]),
            float(data["precio"])
        )

    def __str__(self):
        return f"🆔 ID: {self.id} | 🏷️ Nombre: {self.nombre} | 📦 Cantidad: {self.cantidad} | 💰 Precio: ${self.precio:.2f}"

class Inventario:
    """Contiene y gestiona los productos con guardado persistente usando un diccionario."""

    ARCHIVO_DATOS = "datos_inventario.json"

    def __init__(self):
        self.productos = {}  # ahora usamos un diccionario
        self.cargar_inventario()

    def guardar_inventario(self):
        try:
            with open(self.ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
                productos_dict = {id: p.to_dict() for id, p in self.productos.items()}
                json.dump(productos_dict, archivo, indent=4)
        except PermissionError:
            print("❌ Error: no se tienen permisos para escribir en el archivo.")
        except Exception as e:
            print(f"⚠️ No se pudo guardar el inventario: {e}")

    def cargar_inventario(self):
        if not os.path.exists(self.ARCHIVO_DATOS):
            try:
                with open(self.ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
                    json.dump({}, archivo)
                print("📭 Inventario vacío al iniciar el programa.")
            except PermissionError:
                print("❌ Error: no se tienen permisos para crear el archivo de inventario.")
            return
        try:
            with open(self.ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                self.productos = {id: Producto.from_dict(prod) for id, prod in datos.items()}
                if self.productos:
                    print("📂 Inventario cargado correctamente desde archivo.")
                else:
                    print("📭 Inventario vacío al iniciar.")
        except json.JSONDecodeError:
            print("⚠ Archivo corrupto. Se inicializa inventario vacío.")
            self.productos = {}
        except PermissionError:
            print("❌ Error: no se tienen permisos para leer el archivo.")
        except Exception as e:
            print(f"❌ Error al cargar el archivo de inventario: {e}")
            self.productos = {}

    def agregar_producto(self, producto):
        if producto.id in self.productos:
            return False
        self.productos[producto.id] = producto
        self.guardar_inventario()
        return True

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
            self.guardar_inventario()
            return True
        return False

    def cambiar_cantidad(self, id, nueva_cantidad):
        if id in self.productos:
            self.productos[id].cantidad = nueva_cantidad
            self.guardar_inventario()
            return True
        return False

    def cambiar_precio(self, id, nuevo_precio):
        if id in self.productos:
            self.productos[id].precio = nuevo_precio
            self.guardar_inventario()
            return True
        return False

    def buscar_producto(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]

    def obtener_todos(self):
        return list(self.productos.values())

def menu():
    inventario = Inventario()

    while True:
        print("\n🌟===== MENÚ PRINCIPAL – INVENTARIO DE TIENDA =====🌟")
        print("1️⃣  Añadir nuevo producto")
        print("2️⃣  Eliminar producto por ID")
        print("3️⃣  Actualizar cantidad de producto")
        print("4️⃣  Actualizar precio de producto")
        print("5️⃣  Buscar producto por nombre")
        print("6️⃣  Mostrar todos los productos")
        print("0️⃣  Salir del sistema")

        opcion = input("🔸 Seleccione una opción: ")

        if opcion == "1":
            print("\n➕ Añadir nuevo producto:")
            id = input("🔹 Ingrese ID: ")
            nombre = input("🔹 Ingrese nombre: ")
            try:
                cantidad = int(input("🔹 Ingrese cantidad: "))
                precio = float(input("🔹 Ingrese precio: "))
            except ValueError:
                print("❌ Error: cantidad o precio inválidos.")
                continue
            producto = Producto(id, nombre, cantidad, precio)
            if inventario.agregar_producto(producto):
                print("✅ Producto añadido y guardado correctamente.")
            else:
                print("⚠️ Ya existe un producto con ese ID.")

        elif opcion == "2":
            id = input("\n🔹 Ingrese ID del producto a eliminar: ")
            if inventario.eliminar_producto(id):
                print("✅ Producto eliminado correctamente.")
            else:
                print("❌ Producto no encontrado.")

        elif opcion == "3":
            id = input("\n🔹 Ingrese ID del producto: ")
            try:
                nueva_cantidad = int(input("🔹 Ingrese nueva cantidad: "))
            except ValueError:
                print("❌ Cantidad inválida.")
                continue
            if inventario.cambiar_cantidad(id, nueva_cantidad):
                print("✅ Cantidad actualizada correctamente.")
            else:
                print("❌ Producto no encontrado.")

        elif opcion == "4":
            id = input("\n🔹 Ingrese ID del producto: ")
            try:
                nuevo_precio = float(input("🔹 Ingrese nuevo precio: "))
            except ValueError:
                print("❌ Precio inválido.")
                continue
            if inventario.cambiar_precio(id, nuevo_precio):
                print("✅ Precio actualizado correctamente.")
            else:
                print("❌ Producto no encontrado.")

        elif opcion == "5":
            nombre = input("\n🔹 Ingrese parte del nombre del producto: ")
            resultados = inventario.buscar_producto(nombre)
            if resultados:
                print("📄 Resultados encontrados:")
                for p in resultados:
                    print(p)
            else:
                print("❌ No se encontraron coincidencias.")

        elif opcion == "6":
            productos = inventario.obtener_todos()
            if productos:
                print("\n📦 Productos en inventario:")
                for p in productos:
                    print(p)
            else:
                print("📭 El inventario está vacío.")

        elif opcion == "0":
            print("👋 ¡Gracias por usar el sistema! Hasta luego.")
            break

        else:
            print("⚠️ Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()

