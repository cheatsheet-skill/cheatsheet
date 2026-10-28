# Ejemplo tema 5: suma de una lista de numeros
# El programa pide numeros y los guarda en una lista

cantidad = int(input("¿Cuántos números? "))
numeros = []
i = 0
while i < cantidad:
    num = float(input("Número " + str(i + 1) + ": "))
    numeros.append(num)
    i = i + 1

# recorremos la lista para sumar
suma = 0
for n in numeros:
    suma = suma + n

print("Suma:", suma)

# contamos los positivos
positivos = 0
for n in numeros:
    if n > 0:
        positivos = positivos + 1
print("Positivos:", positivos)
