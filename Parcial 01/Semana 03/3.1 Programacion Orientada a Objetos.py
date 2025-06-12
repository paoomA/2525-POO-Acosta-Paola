# Programa: Promedio Semanal del Clima - POO con mismos datos
# Enfoque: Programación Orientada a Objetos (POO)

# Clase que representa la información diaria del clima
class ClimaDiario:
    def __init__(self, temperatura):
        self.__temperatura = temperatura

    def obtener_temperatura(self):
        return self.__temperatura

    def establecer_temperatura(self, nueva_temp):
        self.__temperatura = nueva_temp

# Clase que representa el clima semanal
class ClimaSemanal:
    def __init__(self):
        self.temperaturas_diarias = []

    def agregar_dia(self, temperatura):
        clima = ClimaDiario(temperatura)
        self.temperaturas_diarias.append(clima)

    def calcular_promedio(self):
        suma = 0
        for clima in self.temperaturas_diarias:
            suma += clima.obtener_temperatura()
        promedio = suma / len(self.temperaturas_diarias)
        return promedio

# Función principal
def main():
    print("=== Promedio Semanal del Clima (POO con mismos datos) ===")

    # Datos idénticos al programa tradicional
    datos_simulados = [22.5, 24.0, 23.8, 25.2, 21.9, 24.6, 23.3]

    semana = ClimaSemanal()

    for temp in datos_simulados:
        semana.agregar_dia(temp)

    promedio = semana.calcular_promedio()
    print(f"Temperaturas: {datos_simulados}")
    print(f"El promedio semanal de temperatura es: {promedio:.2f}°C")

main()