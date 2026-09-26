#menu1
def sumar_tupla(lista):
    suma = 0
    for elemento in lista:
        suma = suma + elemento
    return suma


def procesar_tuplas():
    numeros = (909, 231, 64, 124, 345)

    print(f"\nTercer elemento: {numeros[2]}")

    num1 = int(input("\nIngresa un nuevo número a añadir: "))
    num2 = int(input("Ingresa otro nuevo número a añadir: "))

    nuevos = (num1, num2)
    numeros_actualizados = numeros + nuevos

    print(f"\nNueva tupla: {numeros_actualizados}")

    lista_numeros = list(numeros_actualizados)
    lista_numeros.sort()
    print(f"\nLista ordenada: {lista_numeros}")

    suma_total = sumar_tupla(lista_numeros)
    print(f"\nSuma total: {suma_total}")

#menu2
def buscar_telefono(contactos, nombre):
    return contactos[nombre]

    
def procesar_diccionarios(contactos):
    nuevo_nombre = input("\nNombre del nuevo contacto: ").capitalize()
    nuevo_tel = input("Teléfono del nuevo contacto: ")

    contactos[nuevo_nombre] = nuevo_tel

    nombres = list(contactos.keys())
    nombres_texto = ", ".join(nombres)

    print(f"\nContactos registrados: {nombres_texto}")

    while True:
        buscar_nombre = input("\nNombre a buscar: ").capitalize()
        if buscar_nombre in contactos:
            telefono = buscar_telefono(contactos, buscar_nombre)
            print(f"El teléfono de {buscar_nombre} es: {telefono}")
            break
        else:
            print("Contacto no encontrado.")

contactos = {
    "Esme": "555-3007",
    "Daniel": "555-6705",
    "Axel": "555-1651"
}

#menu3
def procesar_excepciones():
    try:
        numero1 = int(input("\nIngresa el primer número entero: "))
        numero2 = int(input("Ingresa el segundo número entero: "))

        suma = numero1 + numero2
        print(f"\nLa suma de {numero1} + {numero2} es: {suma}")

        try:
            resultado = numero1 / numero2
            print(f"\nLa división de {numero1} entre {numero2} es: {resultado}")
        except ZeroDivisionError:
            print("\nError: no se puede dividir entre cero.")

    except ValueError:
        print("\nError: debes ingresar únicamente números enteros.")

#menu4
def contar_palabras(texto):
    palabras = texto.split()
    return len(palabras)


def procesar_strings():
    mensaje = input("\nEscribe un mensaje: ")

    print(f"\nCantidad de caracteres em el mensaje: {len(mensaje)}")

    mensaje_mayus = mensaje.upper()
    print(f"\nTu mensaje en mayúsculas: {mensaje_mayus}")

    palabra_buscada = input("Palabra que quieres reemplazar: ")
    palabra_nueva = input("Palabra nueva: ")

    posicion = mensaje.lower().find(palabra_buscada.lower())

    if posicion != -1:
        mensaje_reemplazado = mensaje[:posicion] + palabra_nueva + mensaje[posicion + len(palabra_buscada):]
        print(f"Mensaje con la palabra reemplazada: {mensaje_reemplazado}")
    else:
        print("\nLa palabra no se encontró en el mensaje. No se reemplazó.\n")

    total_palabras = contar_palabras(mensaje)
    print(f"El mensaje contiene {total_palabras} palabras")

#menu principal
def mostrar_menu():
    print("\n====== MENÚ PRINCIPAL ======\n")
    print("1. Tuplas")
    print("2. Diccionarios")
    print("3. Excepciones")
    print("4. Strings")
    print("5. Finalizar")


while True:
    mostrar_menu()
    opcion = input("Elige una opción: ")

    if opcion == "1":
        print("\n===TUPLAS===")
        procesar_tuplas()
    elif opcion == "2":
        print("\n===DICCIONARIOS===")
        procesar_diccionarios(contactos)
    elif opcion == "3":
        print("\n===EXCEPCIONES===")
        procesar_excepciones()
    elif opcion == "4":
        print("\n===STRINGS===")
        procesar_strings()
    elif opcion == "5":
        print("\nPrograma finalizado.\n")
        break
    else:
        print("\nOpción no válida, intenta de nuevo.")