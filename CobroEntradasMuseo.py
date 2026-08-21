print("\n==========Bienvenido al Museo de Antropología e Historia==========\n")

num_visitantes = int(input("Ingrese el número de visitantes: "))
total_completo = 0

for i in range(1, num_visitantes + 1):
    print(f"\n======Visitante N. {i}======")
    edad = int(input(f"\n¿Cual es la edad del visitante {i}? "))

    #identificamos edad y asignamos precios
    if edad <= 0:
        print("\nEdad no valida, visitante omitido")
        continue

    if edad < 3:
        precio = 0
        print("\n¡Entrada gratuita!")
        continue

    elif edad <=17:
        precio = 30

    else:
        precio = 45

    #descuentos

    print("\nSeleccione el tipo de visitante:")
    print("1. Adulto mayor 12% Off")
    print("2. Profesor 10% Off")
    print("3. Estudiante 10% Off")
    print("4. Ninguno (Sin descuento)\n")

    while True:

        tipo = int(input("Seleccione una opción (1-4): "))

        if tipo == 1:
            descuento = 0.12
            tipo_descuento = "Adulto mayor (12%)"
            break

        elif tipo == 2:
            descuento = 0.10
            tipo_descuento = "Profesor (10%)"
            break

        elif tipo == 3:
            descuento = 0.10
            tipo_descuento = "Estudiante (10%)"
            break

        elif tipo == 4:
            descuento = 0
            tipo_descuento = "Sin descuento"
            break

        else:
            print("Tipo de visitante no válido. Vuelva a intentar\n")

    monto_descuento = precio * descuento
    precio_con_desc = precio - monto_descuento


    print(f"\n======Resumen de visitante N.{i}======\n")
    print(f"Edad: {edad}")
    print(f"Precio base: ${precio}")
    print(f"Descuento: {tipo_descuento}")
    print(f"Monto descontado: ${monto_descuento:.2f}")
    print(f"Total a pagar: ${precio_con_desc:.2f}")

    #suma de precios
    total_completo += precio_con_desc


print("\n======GRACIAS POR SU COMPRA======")
print(f"\nSu total es: ${total_completo:.2f}")