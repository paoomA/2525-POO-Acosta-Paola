import json
import os

# ==============================
# Clase Libro
# ==============================
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"📖 {self.titulo} de {self.autor} | Categoría: {self.categoria} | ISBN: {self.isbn}"

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "isbn": self.isbn
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["titulo"], data["autor"], data["categoria"], data["isbn"])


# ==============================
# Clase Usuario
# ==============================
class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista de objetos Libro

    def __str__(self):
        return f"👤 Usuario: {self.nombre} | ID: {self.id_usuario}"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "id_usuario": self.id_usuario,
            "libros_prestados": [libro.isbn for libro in self.libros_prestados]
        }

    @classmethod
    def from_dict(cls, data):
        usuario = cls(data["nombre"], data["id_usuario"])
        usuario.libros_prestados = data.get("libros_prestados", [])
        return usuario


# ==============================
# Clase Biblioteca
# ==============================
class Biblioteca:
    def __init__(self):
        self.libros = {}     # isbn: Libro
        self.usuarios = {}   # id_usuario: Usuario
        self.cargar_datos()

    def cargar_datos(self):
        # Cargar libros
        if os.path.exists("libros.json"):
            with open("libros.json", "r") as f:
                libros_data = json.load(f)
                for libro_dict in libros_data:
                    libro = Libro.from_dict(libro_dict)
                    self.libros[libro.isbn] = libro

        # Cargar usuarios
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as f:
                usuarios_data = json.load(f)
                for usuario_dict in usuarios_data:
                    usuario = Usuario.from_dict(usuario_dict)
                    self.usuarios[usuario.id_usuario] = usuario

        # Cargar préstamos y asignar libros prestados
        if os.path.exists("prestamos.json"):
            with open("prestamos.json", "r") as f:
                prestamos_data = json.load(f)
                for user_id, lista_isbns in prestamos_data.items():
                    if user_id in self.usuarios:
                        usuario = self.usuarios[user_id]
                        usuario.libros_prestados = []
                        for isbn in lista_isbns:
                            if isbn in self.libros:
                                usuario.libros_prestados.append(self.libros[isbn])

    def guardar_datos(self):
        with open("libros.json", "w") as f:
            json.dump([libro.to_dict() for libro in self.libros.values()], f, indent=4)

        with open("usuarios.json", "w") as f:
            json.dump([usuario.to_dict() for usuario in self.usuarios.values()], f, indent=4)

        prestamos = {
            usuario.id_usuario: [libro.isbn for libro in usuario.libros_prestados]
            for usuario in self.usuarios.values() if usuario.libros_prestados
        }
        with open("prestamos.json", "w") as f:
            json.dump(prestamos, f, indent=4)

    def agregar_libro(self, libro):
        if libro.isbn not in self.libros:
            self.libros[libro.isbn] = libro
            print(f"✅ Libro agregado: {libro}")
        else:
            print("⚠️ El libro ya está registrado.")

    def registrar_usuario(self, usuario):
        if usuario.id_usuario not in self.usuarios:
            self.usuarios[usuario.id_usuario] = usuario
            print(f"✅ Usuario registrado: {usuario}")
        else:
            print("⚠️ ID de usuario ya existente.")

    def prestar_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios:
            print("⚠️ Usuario no registrado.")
            return
        if isbn not in self.libros:
            print("⚠️ Libro no encontrado.")
            return

        # Verificar si el libro ya está prestado
        for usuario in self.usuarios.values():
            for libro in usuario.libros_prestados:
                if libro.isbn == isbn:
                    print("⚠️ El libro ya está prestado.")
                    return

        usuario = self.usuarios[id_usuario]
        libro = self.libros[isbn]
        usuario.libros_prestados.append(libro)
        print(f"📚 Libro prestado: {libro} ➡️ a {usuario.nombre}")

    def devolver_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios:
            print("⚠️ Usuario no registrado.")
            return

        usuario = self.usuarios[id_usuario]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                print(f"🔄 Libro devuelto: {libro} por {usuario.nombre}")
                return
        print("⚠️ El usuario no tiene prestado ese libro.")

    def buscar_libro(self, **kwargs):
        resultados = []
        for libro in self.libros.values():
            if ("titulo" in kwargs and kwargs["titulo"].lower() in libro.titulo.lower()) \
               or ("autor" in kwargs and kwargs["autor"].lower() in libro.autor.lower()) \
               or ("categoria" in kwargs and kwargs["categoria"].lower() in libro.categoria.lower()):
                resultados.append(libro)

        if resultados:
            print("🔍 Libros encontrados:")
            for l in resultados:
                print(f"   {l}")
        else:
            print("⚠️ No se encontraron coincidencias.")

    def listar_todos_prestados(self):
        encontrados = False
        for usuario in self.usuarios.values():
            for libro in usuario.libros_prestados:
                print(f"📖 {libro} ➡️ prestado a {usuario.nombre}")
                encontrados = True
        if not encontrados:
            print("ℹ️ No hay libros prestados actualmente.")

    def listar_todos_usuarios_y_libros(self):
        print("👥 Usuarios registrados:")
        for usuario in self.usuarios.values():
            print(f"   {usuario}")

        print("\n📚 Libros disponibles:")
        prestados = {libro.isbn for u in self.usuarios.values() for libro in u.libros_prestados}
        for libro in self.libros.values():
            if libro.isbn not in prestados:
                print(f"   {libro}")

# ==============================
# Menú interactivo
# ==============================
if __name__ == "__main__":
    biblioteca = Biblioteca()

    while True:
        print("\n📚 MENÚ BIBLIOTECA")
        print("1. Agregar libro")
        print("2. Registrar usuario")
        print("3. Prestar libro")
        print("4. Devolver libro")
        print("5. Buscar libro")
        print("6. Listar libros prestados")
        print("7. Listar usuarios y libros")
        print("8. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.agregar_libro(libro)
            biblioteca.guardar_datos()

        elif opcion == "2":
            nombre = input("Nombre de usuario: ")
            id_usuario = input("ID de usuario: ")
            usuario = Usuario(nombre, id_usuario)
            biblioteca.registrar_usuario(usuario)
            biblioteca.guardar_datos()

        elif opcion == "3":
            id_usuario = input("ID de usuario: ")
            isbn = input("ISBN del libro a prestar: ")
            biblioteca.prestar_libro(id_usuario, isbn)
            biblioteca.guardar_datos()

        elif opcion == "4":
            id_usuario = input("ID de usuario: ")
            isbn = input("ISBN del libro a devolver: ")
            biblioteca.devolver_libro(id_usuario, isbn)
            biblioteca.guardar_datos()

        elif opcion == "5":
            criterio = input("Buscar por (titulo/autor/categoria): ").lower()
            valor = input(f"Ingrese {criterio}: ")
            biblioteca.buscar_libro(**{criterio: valor})

        elif opcion == "6":
            biblioteca.listar_todos_prestados()

        elif opcion == "7":
            biblioteca.listar_todos_usuarios_y_libros()

        elif opcion == "8":
            print("💾 Guardando y saliendo...")
            biblioteca.guardar_datos()
            break

        else:
            print("❌ Opción inválida.")

