size = 10

tabla = []
for renglon in range(1, size + 1):
    fila = []
    for columna in range(1, size + 1):
        producto = 0
        for numveces in range(columna):
            producto = producto + renglon
        fila.append(producto)
    tabla.append(fila)

def imprimir_tabla(tabla):
    for fila in tabla:
        linea = ""
        for valor in fila:
            linea = linea + str(valor) + "\t"
        print(linea)

def consultar_producto(tabla, renglon, columna):
    return tabla[renglon - 1][columna - 1]

print("\nTabla de pitagoras:")
print("\nIngrese un renlgón y una columna para obtener su producto:\n")

imprimir_tabla(tabla)

renglon = int(input("\nRenglón: "))
columna = int(input("Columna: "))

resultado = consultar_producto(tabla, renglon, columna)
print(f"\nEl producto de {renglon} x {columna} es: {resultado}")