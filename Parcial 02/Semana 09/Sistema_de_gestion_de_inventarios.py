# 📦 SISTEMA DE GESTIÓN DE INVENTARIO DE TIENDA

class Producto:
    """Representa un producto individual en el inventario."""

    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters y setters
    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_cantidad(self):
        return self.cantidad

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        return f"🆔 ID: {self.id} | 🏷️ Nombre: {self.nombre} | 📦 Cantidad: {self.cantidad} | 💰 Precio: ${self.precio:.2f}"


class Inventario:
    """Contiene y gestiona la lista de productos."""

    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        """Añade un producto nuevo si el ID no existe."""
        if any(p.get_id() == producto.get_id() for p in self.productos):
            return False
        self.productos.append(producto)
        return True

    def eliminar_producto(self, id):
        """Elimina un producto por su ID."""
        for p in self.productos:
            if p.get_id() == id:
                self.productos.remove(p)
                return True
        return False

    def actualizar_cantidad(self, id, cantidad):
        """Actualiza la cantidad disponible de un producto."""
        for p in self.productos:
            if p.get_id() == id:
                p.set_cantidad(cantidad)
                return True
        return False

    def actualizar_precio(self, id, precio):
        """Modifica el precio de un producto."""
        for p in self.productos:
            if p.get_id() == id:
                p.set_precio(precio)
                return True
        return False

    def buscar_producto(self, nombre):
        """Busca productos por nombre (coincidencia parcial)."""
        return [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]

    def mostrar_productos(self):
        """Devuelve todos los productos disponibles en el inventario."""
        return self.productos


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
                print("✅ Producto añadido correctamente.")
            else:
                print("⚠️ Error: ya existe un producto con ese ID.")

        elif opcion == "2":
            print("\n🗑️ Eliminar producto:")
            id = input("🔹 Ingrese ID del producto a eliminar: ")
            if inventario.eliminar_producto(id):
                print("✅ Producto eliminado correctamente.")
            else:
                print("❌ Producto no encontrado.")

        elif opcion == "3":
            print("\n🔄 Actualizar cantidad:")
            id = input("🔹 Ingrese ID del producto: ")
            try:
                cantidad = int(input("🔹 Ingrese nueva cantidad: "))
            except ValueError:
                print("❌ Cantidad inválida.")
                continue
            if inventario.actualizar_cantidad(id, cantidad):
                print("✅ Cantidad actualizada correctamente.")
            else:
                print("❌ Producto no encontrado.")

        elif opcion == "4":
            print("\n💲 Actualizar precio:")
            id = input("🔹 Ingrese ID del producto: ")
            try:
                precio = float(input("🔹 Ingrese nuevo precio: "))
            except ValueError:
                print("❌ Precio inválido.")
                continue
            if inventario.actualizar_precio(id, precio):
                print("✅ Precio actualizado correctamente.")
            else:
                print("❌ Producto no encontrado.")

        elif opcion == "5":
            print("\n🔍 Buscar producto:")
            nombre = input("🔹 Ingrese parte del nombre: ")
            resultados = inventario.buscar_producto(nombre)
            if resultados:
                print("📄 Resultados encontrados:")
                for p in resultados:
                    print(p)
            else:
                print("❌ No se encontraron coincidencias.")

        elif opcion == "6":
            print("\n📦 Inventario completo:")
            productos = inventario.mostrar_productos()
            if productos:
                for p in productos:
                    print(p)
            else:
                print("📭 El inventario está vacío.")

        elif opcion == "0":
            print("👋 ¡Gracias por usar el sistema! Hasta luego.")
            break

        else:
            print("⚠️ Opción inválida. Intente nuevamente.")


# Punto de entrada del programa
if __name__ == "__main__":
    menu()
