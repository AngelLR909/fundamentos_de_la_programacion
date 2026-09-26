import time        # Para pausas de la pantalla de carga y conteo de inactividad
import threading   # Permite contar la inactividad mientras input() espera

# Segundos de inactividad permitidos (10 min = 600 s).
# Para probarlo sin esperar los 600 seg, se puede cambiar a un valor menor
TIEMPO_INACTIVIDAD = 600

# Req. 7: diccionario con los reportes disponibles
REPORTES = {
    "reporte_ventas.txt": "Detalle de cada venta registrada",
    "corte_caja.txt": "Historial de cortes de caja",
    "reporte_devoluciones.txt": "Devoluciones registradas",
    "reporte_metodos_pago.txt": "Ventas separadas en efectivo y tarjeta",
}

# Req. 4: menú principal en forma de matriz. ["Clave númerica de la opción", "Nombre de la opcion"]
MENU = [
    ["1", "Registrar venta"],
    ["2", "Registrar devolucion"],
    ["3", "Corte de caja"],
    ["4", "Reportes"],
    ["5", "Salir"],
]


# ------------------ FUNCIONES ------------------

# Funcion para solicitar números decimales. Repetirá la pregunta hasta obtener número decimal (float)
def pedir_decimal(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Dato invalido. Escribe solo numeros, incluyendo decimales.")

# Funcion para solicitar enteros. Similar a la de decimales, repetirá hasta que el dato sea entero (int)
def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Dato invalido. Escribe número entero")

# Funcion que recibirá la tupla de la fecha y la convertirá a texto 
def fecha_a_texto(fecha):
    # Convierte la tupla (dd, mm, aaaa) en el texto "dd/mm/aaaa"
    return f"{fecha[0]:02d}/{fecha[1]:02d}/{fecha[2]}"


# ------------------ PANTALLA DE INICIO ------------------

# Req. 1: Identificación del usuario. La funcion se hace en un ciclo while para evitar campo en blanco
def pedir_nombre():
    nombre = input("Ingresa tu nombre: ").strip().title()
    while nombre == "":
        nombre = input("El nombre no puede quedar vacio. Ingresa tu nombre: ").strip().title()
    return nombre


# Req. 2: Función de bienvenida usando operadores de cadenas.
def mostrar_bienvenida(cajero):
    linea = "=" * 55
    mensaje = "Bienvenido(a), " + cajero + ". Tu turno como cajero ha iniciado."
    print("\n" + linea)
    print(mensaje)
    print("Sistema de caja - Minisuper | El Puy")
    print(linea)


# Req. 3: pantalla de carga. Cada paso añade 1 seg  
def pantalla_de_carga():
    pasos = [
        "Iniciando sistema",
        "Cargando modulo de ventas",
        "Cargando modulo de devoluciones",
        "Verificando archivos de reportes",
        "Preparando menu principal",
    ]
    total_pasos = len(pasos)

    print("\nCargando, por favor espera...")
    for i in range(total_pasos): #ciclo para imprimir una barra de progreso visual con los pasos
        avance = i + 1
        barra = "#" * avance + "-" * (total_pasos - avance)
        porcentaje = avance * 100 // total_pasos
        print("[" + barra + "] " + str(porcentaje) + "%  " + pasos[i] + "...")
        time.sleep(1)
    print("Sistema listo.\n")


# Req. 6: Fecha de operacion. Función para solicitar la fecha y corregir formato o días/meses invslidos
def pedir_fecha():
    while True:
        texto = input("Ingresa la fecha de operacion (dd/mm/aaaa): ").strip()

        texto = texto.replace("-", "/") #utilizamos .replace() para convertir estos caracteres en /
        texto = texto.replace(" ", "/") #en caso de que el usuario escriba la fecha con espacios o guiones
        partes = texto.split("/")

        if len(partes) != 3:
            print("Formato incorrecto. Ejemplo valido: 24/09/2026")
            continue

        try:
            dd = int(partes[0])
            mm = int(partes[1])
            aaaa = int(partes[2])
        except ValueError:
            print("La fecha solo debe contener numeros. Ejemplo: 24/09/2026")
            continue

        # if para evitar fechas como 69/09 o 13/67 y aceptar unicamente el año en 4 digitos
        if dd < 1 or dd > 31 or mm < 1 or mm > 12 or len(partes[2]) != 4: 
            print("Fecha fuera de rango. Dia 1-31, mes 1-12 y año de 4 digitos.")
            continue

        fecha = dd, mm, aaaa
        return fecha


# ------------------ MENÚ ------------------

# Funcion que recorre la matriz para mostrar las opciones
def mostrar_menu(cajero, fecha):
    print("\n+-+---------------------------")
    for fila in MENU:
        print("|" + fila[0] + "| " + fila[1])
    print("+-+---------------------------\n")
    print("Cajero: " + cajero + "  |  Fecha: " + fecha_a_texto(fecha))


# La seleccion tambien se hace recorriendo la matriz mediante una funcion que regresa valor, así
# podemos identificiar si se encontró la opcion
def buscar_opcion(opcion):
    for fila in MENU:
        if fila[0] == opcion:
            return fila
    return None


# Req. 5: esta funcion corre "en paralelo" (en un hilo) mientras el
# programa espera el input del menu. Cuenta segundo a segundo con un for.
# "estado" es un diccionario que comparte con el programa principal.
def contar_inactividad(estado):
    for segundo in range(TIEMPO_INACTIVIDAD):
        time.sleep(1)
        if estado["respondio"]: # if para indicar si el usuario ya eligió una opción, deteniendo el conteo
            return

    # En cuanto el `for` termine, osea, pasaron los 10 minutos sin respuesta, se mostrará el mensaje de inactividad
    estado["inactivo"] = True
    print("\n*** Menu suspendido: pasaron 10 minutos sin actividad. ***")
    print("¿Deseas continuar en el menú? (Si/No)")


# ------------------ ARCHIVOS ------------------

# Funcion para concentrar la escritura de todos los reportes
def guardar_en_archivo(nombre_archivo, lineas, fecha): # Req. 6: la fecha de la tupla se integra en cada registro.
    
    try:
        # Modo "a" para agrega al final del archivo sin borrar lo anterior.
        # Importante, se agrega encoding="utf-8" para prevenir caracteres raros,
        # así evitamos caracteres raros como al escribir el apellido Peña por ejemplo
        with open(nombre_archivo, "a", encoding="utf-8") as archivo:
            archivo.write("Fecha de operacion: " + fecha_a_texto(fecha) + "\n")
            for linea in lineas:
                archivo.write(linea + "\n")
            archivo.write("-" * 40 + "\n")
        print("\nRegistro guardado en " + nombre_archivo)
    except PermissionError:
        print("[ERROR] No hay permisos para escribir en " + nombre_archivo + ".")
    except OSError:
        print("[ERROR] No se pudo guardar la informacion en " + nombre_archivo + ".")

# Función para mostrar los archivos disponibles del diccionario REPORTES
def ver_reportes():
    print("\n--- Reportes disponibles ---")
    for nombre in REPORTES:
        print("- " + nombre + "  ->  " + REPORTES[nombre])

    nombre_archivo = input("\nEscribe el nombre del reporte que deseas abrir: ").strip().lower()
    if nombre_archivo == "":
        print("No escribiste ningún nombre.")
        return

    # Si el usuario no escribio la extension, se le agrega
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo = nombre_archivo + ".txt"

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        print("\n========== " + nombre_archivo + " ==========")
        if contenido.strip() == "":
            print("(El reporte esta vacio, aun no hay registros)")
        else:
            print(contenido)

    except FileNotFoundError:
        print("[ERROR] El archivo '" + nombre_archivo + "' no existe. Revisa que el nombre este bien escrito.")
    except PermissionError:
        print("[ERROR] No hay permisos para abrir '" + nombre_archivo + "'.")
    except UnicodeDecodeError:
        print("[ERROR] El archivo tiene un formato que no se puede leer como texto.")
    except OSError:
        print("[ERROR] Ocurrio un problema inesperado al abrir el archivo.")


# ------------------ OPCIONES DEL MENU ------------------

def registrar_venta(turno, cajero, fecha):
    print("\n--- Nueva Venta ---")
    print("Digita 0 para terminar de agregar productos.")

    subtotal_venta = 0.0
    articulos = 0

    while True:
        precio_unitario = pedir_decimal("Precio unitario del producto ($): ")

        if precio_unitario == 0:
            break
        if precio_unitario < 0:
            print("El precio no puede ser negativo.\n")
            continue

        cantidad = pedir_entero("Cantidad comprada: ")
        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0. Vuelve a capturar.\n")
            continue

        subtotal_producto = precio_unitario * cantidad
        subtotal_venta += subtotal_producto
        articulos += cantidad
        print(f"-> Subtotal parcial de este producto: ${subtotal_producto:.2f}\n")

    if subtotal_venta == 0:
        print("Venta cancelada: no se agrego ningun producto.")
        return

    # Descuentos del prototipo inicial
    if subtotal_venta > 500:
        descuento = subtotal_venta * 0.10
    elif subtotal_venta > 200:
        descuento = subtotal_venta * 0.05
    else:
        descuento = 0.0

    total_venta = subtotal_venta - descuento

    # Mostramos el total para que el cajero pueda visualizar cuanto debe cobrar antes
    print(f"\nSubtotal general: ${subtotal_venta:.2f}")
    print(f"Descuento aplicado: ${descuento:.2f}")
    print(f"Total a cobrar: ${total_venta:.2f}")

    metodo = ""
    while metodo == "":
        print("\nMetodo de pago:  1. Efectivo   2. Tarjeta")
        opcion_pago = input("Elige el metodo de pago (1-2): ").strip()
        if opcion_pago == "1":
            metodo = "Efectivo"
        elif opcion_pago == "2":
            metodo = "Tarjeta"
        else:
            print("Opcion invalida.")

    pago_cliente = total_venta
    cambio = 0.0
    if metodo == "Efectivo":
        pago_cliente = pedir_decimal("Monto con el que paga el cliente ($): ")
        while pago_cliente < total_venta:
            faltante = total_venta - pago_cliente
            print(f"El monto no alcanza, faltan ${faltante:.2f}")
            pago_cliente = pedir_decimal("Monto con el que paga el cliente ($): ")
        cambio = pago_cliente - total_venta

    # Actualizador de acumulados del turno
    turno["transacciones"] += 1
    turno["ventas"] += total_venta
    if metodo == "Efectivo":
        turno["efectivo"] += total_venta
    else:
        turno["tarjeta"] += total_venta
    folio = turno["transacciones"]

    print("\n=================================")
    print("--- Ticket de Venta ---")
    print("Folio: " + str(folio))
    print(f"Subtotal general: ${subtotal_venta:.2f}")
    print(f"Descuento aplicado: ${descuento:.2f}")
    print(f"Total a cobrar: ${total_venta:.2f}")
    print("Metodo de pago: " + metodo)
    if metodo == "Efectivo":
        print(f"Recibido: ${pago_cliente:.2f}")
        print(f"Cambio a entregar: ${cambio:.2f}")
    print("=================================")
    
    # Escritura en reporte_ventas.txt
    lineas_venta = [
        "Folio de venta: " + str(folio),
        "Cajero: " + cajero,
        "Articulos: " + str(articulos),
        f"Subtotal: ${subtotal_venta:.2f}",
        f"Descuento: ${descuento:.2f}",
        f"Total: ${total_venta:.2f}",
        "Metodo de pago: " + metodo,
    ]
    guardar_en_archivo("reporte_ventas.txt", lineas_venta, fecha)

    # Escritura en reporte_metodos_pago.txt
    lineas_pago = [
        "Folio de venta: " + str(folio),
        "Metodo de pago: " + metodo,
        f"Total cobrado: ${total_venta:.2f}",
    ]
    if metodo == "Efectivo":
        lineas_pago.append(f"Recibido: ${pago_cliente:.2f}")
        lineas_pago.append(f"Cambio: ${cambio:.2f}")
    guardar_en_archivo("reporte_metodos_pago.txt", lineas_pago, fecha)

# Funcion para pedir los detalles de la devolución a registrar
def registrar_devolucion(turno, cajero, fecha):
    print("\n--- Registrar Devolucion ---")

    producto = input("Producto devuelto: ").strip() # Esta informacion unicamente es de referencia para el registro
    while producto == "":
        producto = input("Escribe el nombre del producto devuelto: ").strip()

    monto = pedir_decimal("Monto a devolver ($): ") # Esta info si tiene impacto en la venta
    while monto <= 0:
        print("El monto debe ser mayor a 0.")
        monto = pedir_decimal("Monto a devolver ($): ")

    motivo = input("Motivo de la devolucion: ").strip() # tampoco tiene impacto, solo es informativa
    if motivo == "":
        motivo = "Sin especificar" #No pedimos volver a ingresar como con producto en caso de no tener claro el motivo
    #acumulador
    turno["devoluciones"] += monto
    turno["num_devoluciones"] += 1

    print(f"Devolucion registrada: ${monto:.2f}")

    lineas = [
        "Devolucion No.: " + str(turno["num_devoluciones"]),
        "Cajero: " + cajero,
        "Producto: " + producto,
        f"Monto devuelto: ${monto:.2f}",
        "Motivo: " + motivo,
    ]
    guardar_en_archivo("reporte_devoluciones.txt", lineas, fecha)

# funcion para mostrar el corte de caja del cajero, se detallan montos en efectivo, tarjeta y devoluciones
def corte_de_caja(turno, cajero, fecha):
    total_neto = turno["ventas"] - turno["devoluciones"]

    lineas = [
        "Cajero: " + cajero,
        "Ventas registradas: " + str(turno["transacciones"]),
        f"Ventas en efectivo: ${turno['efectivo']:.2f}",
        f"Ventas con tarjeta: ${turno['tarjeta']:.2f}",
        f"Total vendido: ${turno['ventas']:.2f}",
        "Devoluciones: " + str(turno["num_devoluciones"]),
        f"Total devuelto: ${turno['devoluciones']:.2f}",
        f"Total neto del turno: ${total_neto:.2f}",
    ]

    print("\n--- Corte de Caja ---")
    print("Fecha: " + fecha_a_texto(fecha))
    for linea in lineas:
        print(linea)

    guardar_en_archivo("corte_caja.txt", lineas, fecha)

# ============================== PROGRAMA PRINCIPAL ================================

# Acumulados del turno (un diccionario para poder modificarlos
# desde las funciones sin usar variables globales)
turno = {
    "ventas": 0.0,
    "transacciones": 0,
    "efectivo": 0.0,
    "tarjeta": 0.0,
    "devoluciones": 0.0,
    "num_devoluciones": 0,
}

programa_activo = True
while programa_activo:

    # ---------- Pantalla de inicio ----------
    print("\n=== Sistema de caja - Minisuper | El Puy ===")
    cajero = pedir_nombre()
    mostrar_bienvenida(cajero)
    pantalla_de_carga()
    fecha = pedir_fecha()
    print("Fecha registrada: " + fecha_a_texto(fecha))

    # ---------- Menu principal ----------
    en_menu = True
    while en_menu:
        mostrar_menu(cajero, fecha)

        # Req. 5: cada vez que se muestra el menu arranca un contador nuevo
        estado = {"respondio": False, "inactivo": False}
        contador = threading.Thread(target=contar_inactividad, args=(estado,))
        contador.daemon = True   # Si el programa termina, el contador tambien
        contador.start()

        opcion = input("Elige una opcion (1-5): ").strip()
        estado["respondio"] = True

        if estado["inactivo"]:
            respuesta = opcion.title()
            while respuesta != "Si" and respuesta != "No":
                respuesta = input("Por favor, indica \"si\"/\"no\" ").strip().title()

            if respuesta == "No":
                print("\nRegresando a la pantalla de inicio...")
                en_menu = False
            continue   # Con "Si" se vuelve a mostrar el menu

        fila = buscar_opcion(opcion)
        if fila is None:
            print("Opcion invalida, intenta de nuevo.")
            continue

        clave = fila[0]
        if clave == "1":
            registrar_venta(turno, cajero, fecha)
        elif clave == "2":
            registrar_devolucion(turno, cajero, fecha)
        elif clave == "3":
            corte_de_caja(turno, cajero, fecha)
        elif clave == "4":
            ver_reportes()
        elif clave == "5":
            print("\nCerrando turno...")
            print("Total de transacciones: " + str(turno["transacciones"]))
            print(f"Total vendido: ${turno['ventas']:.2f}")
            en_menu = False
            programa_activo = False

print("\nSistema cerrado exitosamente\n")