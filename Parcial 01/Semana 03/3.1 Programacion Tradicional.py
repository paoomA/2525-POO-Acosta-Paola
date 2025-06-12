# Programa: Promedio Semanal del Clima - Variante 2
# Enfoque: Programación Tradicional
# Objetivo: Calcular el promedio semanal del clima con diferentes datos simulados

# Función para obtener temperaturas simuladas (sin entrada manual)
def ingresar_temperaturas():
    # Nuevo conjunto de temperaturas simuladas
    temperaturas = [22.5, 24.0, 23.8, 25.2, 21.9, 24.6, 23.3]
    return temperaturas

# Función que calcula el promedio semanal de temperaturas
def calcular_promedio(temperaturas):
    suma = sum(temperaturas)
    promedio = suma / len(temperaturas)
    return promedio

# Función principal
def main():
    print("=== Promedio Semanal del Clima (Programación Tradicional - Variante 2) ===")
    temperaturas = ingresar_temperaturas()
    promedio = calcular_promedio(temperaturas)
    print(f"Temperaturas registradas: {temperaturas}")
    print(f"El promedio semanal de temperatura es: {promedio:.2f}°C")

main()