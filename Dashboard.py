import os

def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    print(f"Intentando abrir: {ruta_script_absoluta}")  # Para depurar ruta
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            print("\n--- Resultado de la ejecución ---\n")
            exec(codigo, globals())
    except FileNotFoundError:
        print("El archivo no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer o ejecutar el archivo: {e}")

def mostrar_menu():
    ruta_base = os.path.dirname(__file__)

    opciones = {
        '1': 'Parcial 01/Semana 02/2.1. Tarea semana 02.py',
        '2': 'Parcial 01/Semana 03/3.1 Programacion Orientada a Objetos.py',
        '3': 'Parcial 01/Semana 03/3.1 Programacion Tradicional.py',
        '4': 'Parcial 01/Semana 04/EjemplosMundoReal_POO.py',
        '5': 'Parcial 01/Semana 05/Calculadora de área y perímetro de rectángulo.py',
        '6': 'Parcial 01/Semana 06/Tarea_poo_escuela.py',
        '7': 'Parcial 01/Semana 07/Constructores_init__Destructores_del_.py'
    }

    while True:
        print("\nMenu Principal - Dashboard")
        for key in opciones:
            print(f"{key} - {opciones[key]}")
        print("0 - Salir")

        eleccion = input("Elige un script para ver su código o '0' para salir: ")
        if eleccion == '0':
            break
        elif eleccion in opciones:
            ruta_script = os.path.join(ruta_base, opciones[eleccion])
            mostrar_codigo(ruta_script)
            input("\nPresiona Enter para regresar al menú...")
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()