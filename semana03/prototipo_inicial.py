total_ventas = 0.0
numero_transacciones = 0

print("=== Sistema de caja - Minisuper | El Puy ===")

continuar = True
while continuar:
    print("\n--- Menu ---")
    print("1. Registrar venta")
    print("2. Ver corte de caja")
    print("3. Salir")
    opcion = input("Elige una opcion (1-3): ")

    if opcion == "1":
        print("\n--- Nueva Venta ---")
        print("Digita 0 para terminar de agregar productos.")
        
        subtotal_venta = 0.0
        
        while True:
            precio_unitario = float(input("Precio unitario del producto ($): "))

            if precio_unitario == 0:
                break
                
            cantidad = int(input("Cantidad comprada: "))
            
            subtotal_producto = precio_unitario * cantidad
            subtotal_venta += subtotal_producto
            print(f"-> Subtotal parcial de este producto: ${subtotal_producto:.2f}\n")

        if subtotal_venta > 500:
            descuento = subtotal_venta * 0.10
        elif subtotal_venta > 200:
            descuento = subtotal_venta * 0.05
        else:
            descuento = 0.0

        total_venta = subtotal_venta - descuento

        total_ventas = total_ventas + total_venta
        numero_transacciones = numero_transacciones + 1

        print("\n--- Ticket de Venta ---")
        print(f"Subtotal general: ${subtotal_venta:.2f}")
        print(f"Descuento aplicado: ${descuento:.2f}")
        print(f"Total a cobrar: ${total_venta:.2f}")

    elif opcion == "2":
        print(f"\nVentas registradas: {numero_transacciones}")
        print(f"Total acumulado del turno: ${total_ventas:.2f}")

    elif opcion == "3":
        print("\nCerrando turno...")
        print(f"\nTotal de transacciones: {numero_transacciones}")
        print(f"Total vendido: ${total_ventas:.2f}")
        break

    else:
        print("Opcion invalida, intenta de nuevo.")

print("\nSistema cerrado exitosamente\n")