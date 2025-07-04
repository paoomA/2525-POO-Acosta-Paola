# tarea_poo_escuela.py

# Clase base
class Persona:
    def __init__(self, nombre, edad):
        self._nombre = nombre  # Encapsulación
        self._edad = edad      # Encapsulación

    def presentarse(self):  # Polimorfismo: será sobrescrito
        return f"Hola, soy {self._nombre}."

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre


# Clase derivada: Estudiante
class Estudiante(Persona):
    def __init__(self, nombre, edad, grado, anio_escolar):
        super().__init__(nombre, edad)
        self._grado = grado
        self._anio_escolar = anio_escolar

    def presentarse(self):  # Polimorfismo
        return f"Hola, soy {self._nombre}, estudio en {self._grado} grado en el año {self._anio_escolar}."

    def get_anio_escolar(self):
        return self._anio_escolar


# Clase derivada: Maestra
class Maestra(Persona):
    def __init__(self, nombre, edad, materia):
        super().__init__(nombre, edad)
        self._materia = materia

    def presentarse(self):  # Polimorfismo
        return f"Hola, soy la maestra {self._nombre}, tengo {self._edad} años y enseño {self._materia}."


# Crear instancias
maestra = Maestra("María", 28, "Lengua y Literatura")
estudiante1 = Estudiante("José", 14, "9°", 2025)

# Demostrar funcionamiento
print(maestra.presentarse())           # Clase derivada: Maestra
print(estudiante1.presentarse())       # Clase derivada: Estudiante

# Encapsulación: usar getters y setters
print(estudiante1.get_nombre())
estudiante1.set_nombre("Luis")
print(estudiante1.get_nombre())

# Mostrar año escolar
print(f"Año escolar: {estudiante1.get_anio_escolar()}")