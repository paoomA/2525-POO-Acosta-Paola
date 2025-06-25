# Calculadora de área y perímetro de un triángulo
# Este programa solicita al usuario los lados y la altura de un triángulo,
# calcula el área y el perímetro, y muestra los resultados.
# Se usan tipos de datos: float, string, integer y boolean.
# Los identificadores siguen la convención snake_case.
# Incluye comentarios para mayor comprensión.

def calcular_area_triangulo(base: float, altura: float) -> float:
    return (base * altura) / 2

def calcular_perimetro_triangulo(lado1: float, lado2: float, base: float) -> float:
    return lado1 + lado2 + base

print("Calculadora de área y perímetro de un triángulo")

usuario_nombre = input("Por favor, ingresa tu nombre: ")
base_texto = input("Ingresa la base del triángulo en cm: ")
altura_texto = input("Ingresa la altura del triángulo en cm: ")
lado1_texto = input("Ingresa el primer lado del triángulo en cm: ")
lado2_texto = input("Ingresa el segundo lado del triángulo en cm: ")

# Conversión de entradas de texto a tipo float
base = float(base_texto)
altura = float(altura_texto)
lado1 = float(lado1_texto)
lado2 = float(lado2_texto)

# Cálculo del área y perímetro
area_triangulo = calcular_area_triangulo(base, altura)
perimetro_triangulo = calcular_perimetro_triangulo(lado1, lado2, base)

# Mostrar resultados
print(f"\nHola, {usuario_nombre}.")
print(f"El área del triángulo es: {area_triangulo} cm²")
print(f"El perímetro del triángulo es: {perimetro_triangulo} cm")

programa_ejecuto_bien = True
print(f"¿El programa se ejecutó correctamente? {programa_ejecuto_bien}")
