# Clase que representa una plataforma web de diseño
class PlataformaWeb:
    # Constructor: inicializa el nombre de la plataforma y muestra mensaje de inicio
    def __init__(self, nombre):
        self.nombre = nombre
        print(f"🌐 Plataforma de diseño web '{self.nombre}' ha sido lanzada.")

    # Muestra el estado actual de la plataforma web
    def mostrar_estado(self):
        print(f"✅ Plataforma '{self.nombre}' funcionando correctamente.")

    # Destructor: muestra mensaje cuando la plataforma se cierra
    def __del__(self):
        print(f"🛑 Plataforma '{self.nombre}' ha sido cerrada y sus recursos liberados.")

class DiseñadorWeb:
    # Constructor: crea una diseñadora con nombre, edad y especialidad
    def __init__(self, nombre, edad, especialidad):
        self.nombre = nombre
        self.edad = edad
        self.especialidad = especialidad
        print(f"👩‍💻 Diseñadora '{self.nombre}', {self.edad} años, con especialidad en {self.especialidad} ha iniciado sesión.")

    # Muestra el portafolio del diseñador con su especialidad
    def presentar_portafolio(self):
        print(f"🎨 {self.nombre}, de {self.edad} años, está mostrando su portafolio en {self.especialidad}...")

    # Destructor: muestra mensaje cuando la diseñadora se elimina
    def __del__(self):
        print(f"👋 Diseñadora '{self.nombre}' ha cerrado sesión y fue eliminada del sistema.")

if __name__ == "__main__":
    print("🔧 Iniciando sistema de diseño web - 2025\n")

    plataforma = PlataformaWeb("P-WebDesign")
    plataforma.mostrar_estado()

    diseñadora = DiseñadorWeb("Paolita Acosta", 20, "interfaces responsivas")
    diseñadora.presentar_portafolio()

    print("\n📴 Fin del programa. Cerrando sesión...")