# Programa que modela una librería virtual usando POO en Python

class Producto:
    """
    Representa un producto en la librería.
    Atributos:
        codigo (str): Identificador único del producto.
        nombre (str): Nombre del libro.
        precio (float): Precio unitario.
        stock (int): Cantidad disponible.
    """
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def mostrar_info(self):
        """
        Muestra la información del libro.
        """
        print(f"Código: {self.codigo} | Título: {self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock}")

    def actualizar_stock(self, cantidad):
        """
        Actualiza el stock restando la cantidad vendida.
        """
        if cantidad <= self.stock:
            self.stock -= cantidad
            return True
        else:
            print(f"Stock insuficiente para el libro '{self.nombre}'.")
            return False


class Cliente:
    """
    Representa un cliente que realiza compras en la librería.
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.carrito = {}

    def agregar_al_carrito(self, producto, cantidad):
        """
        Agrega libros al carrito de compra.
        """
        if producto.actualizar_stock(cantidad):
            if producto.codigo in self.carrito:
                self.carrito[producto.codigo]['cantidad'] += cantidad
            else:
                self.carrito[producto.codigo] = {'producto': producto, 'cantidad': cantidad}
            print(f"{cantidad} unidad(es) de '{producto.nombre}' agregada(s) al carrito de {self.nombre}.")
        else:
            print(f"No se pudo agregar '{producto.nombre}' al carrito de {self.nombre}.")

    def mostrar_carrito(self):
        """
        Muestra los libros en el carrito con cantidades y total.
        """
        print(f"\nCarrito de {self.nombre}:")
        total = 0
        for item in self.carrito.values():
            producto = item['producto']
            cantidad = item['cantidad']
            subtotal = producto.precio * cantidad
            total += subtotal
            print(f"- {producto.nombre}: {cantidad} x ${producto.precio:.2f} = ${subtotal:.2f}")
        print(f"Total a pagar: ${total:.2f}")


class Libreria:
    """
    Representa la librería con su catálogo y clientes.
    """
    def __init__(self):
        self.catalogo = []
        self.clientes = []

    def agregar_producto(self, producto):
        """
        Agrega un libro al catálogo de la librería.
        """
        self.catalogo.append(producto)

    def mostrar_catalogo(self):
        """
        Muestra todos los libros disponibles en la librería.
        """
        print("\nCatálogo de libros disponibles:")
        for producto in self.catalogo:
            producto.mostrar_info()

    def registrar_cliente(self, cliente):
        """
        Registra un nuevo cliente en la librería.
        """
        self.clientes.append(cliente)


# Programa principal
if __name__ == "__main__":
    libreria = Libreria()

    # Crear productos (libros) y agregarlos al catálogo
    libro1 = Producto("L001", "El Principito", 9.99, 25)
    libro2 = Producto("L002", "Cien Años de Soledad", 14.50, 15)
    libro3 = Producto("L003", "1984", 12.75, 20)

    libreria.agregar_producto(libro1)
    libreria.agregar_producto(libro2)
    libreria.agregar_producto(libro3)

    libreria.mostrar_catalogo()

    # Crear clientes
    cliente1 = Cliente("Dayana")
    cliente2 = Cliente("Anderson")

    libreria.registrar_cliente(cliente1)
    libreria.registrar_cliente(cliente2)

    # Clientes agregan libros al carrito
    cliente1.agregar_al_carrito(libro1, 2)
    cliente1.agregar_al_carrito(libro3, 1)

    cliente2.agregar_al_carrito(libro2, 1)
    cliente2.agregar_al_carrito(libro3, 2)

    # Mostrar carritos
    cliente1.mostrar_carrito()
    cliente2.mostrar_carrito()