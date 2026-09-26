# Proyecto Final: Sistema de caja - Minisuper El Puy
## Punto de venta con persistencia en archivos de texto
### Descripción del reto
Nuestro programa es un sistema de caja para el Minisuper El Puy, construido a partir del prototipo inicial. Al iniciar identifica al cajero, lo recibe con una bienvenida, muestra una pantalla de carga y solicita la fecha de operación. Después despliega un menú en forma de matriz desde el cual se registran ventas y devoluciones, se genera el corte de caja y se consultan los reportes. Toda la información se guarda de forma permanente en cuatro archivos de texto que deben existir en la misma carpeta del programa: `reporte_ventas.txt`, `corte_caja.txt`, `reporte_devoluciones.txt` y `reporte_metodos_pago.txt`. Además, el menú cuenta con un control de inactividad de 10 minutos.

### Configuración general
1. Importamos los módulos `time` y `threading`, ambos incluidos en Python.
```python
import time        # Para pausas de la pantalla de carga y conteo de inactividad
import threading   # Permite contar la inactividad mientras input() espera
```

#### ¿Qué son y cómo funcionan?
- **`time`** es un módulo para trabajar con el tiempo. Su función `time.sleep(segundos)` detiene la ejecución durante los segundos indicados y después continúa con la siguiente línea.
- **`threading`** es un módulo que permite ejecutar funciones en *hilos*. Un hilo es una tarea que corre al mismo tiempo que el programa principal. Se crea con `threading.Thread(target=funcion, args=(...))`, donde `target` es la función que ejecutará el hilo y `args` es una tupla con sus argumentos. El método `.start()` pone en marcha el hilo, y el programa principal continúa sin esperar a que termine. Marcar el hilo con `daemon = True` hace que se detenga automáticamente cuando el programa principal termina.

#### ¿Qué harán en el código?
- **`time`** genera la pausa de 1 segundo en cada paso de la pantalla de carga, y la pausa de 1 segundo en cada vuelta del `for` de `contar_inactividad`, de modo que cada vuelta del ciclo equivale a un segundo.
- **`threading`** ejecuta la función `contar_inactividad` en un hilo aparte mientras el menú principal espera la opción del usuario con `input()`. Ambos comparten el diccionario `estado`, que les permite saber si el usuario ya respondió o si se cumplió el tiempo de inactividad.

#### ¿Por qué se implementaron?
`input()` detiene todo el programa hasta que el usuario presiona Enter; mientras espera, ninguna otra línea se ejecuta. Por eso, un ciclo `for` en el programa principal no podría medir el tiempo de inactividad del menú. Con `threading`, el conteo corre en paralelo al `input()`, y con `time` cada vuelta del `for` dura un segundo, lo que permite medir los 10 minutos. `time` también se requería para la pausa de la pantalla de carga.

2. Definimos la constante `TIEMPO_INACTIVIDAD` en 600 segundos (10 minutos), el diccionario `REPORTES`, que relaciona el nombre de cada archivo con su descripción, y la matriz `MENU`, una lista de listas donde cada fila contiene la clave de la opción y su nombre.
```python
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
```

### Funciones de apoyo
3. `pedir_decimal` y `pedir_entero` repiten la pregunta dentro de un `while True` hasta que el dato se pueda convertir a `float` o `int`. Si el usuario escribe texto, `except ValueError` muestra un aviso y el ciclo vuelve a preguntar; cuando la conversión es correcta, `return` regresa el valor y termina el ciclo.
4. `fecha_a_texto` recibe la tupla de la fecha y la regresa como texto `dd/mm/aaaa`. El formato `:02d` agrega un cero a la izquierda cuando el día o el mes tienen un solo dígito.
```python
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
```

### Pantalla de inicio
5. `pedir_nombre` captura el nombre del cajero (Req. 1). `.strip()` elimina los espacios al inicio y al final, y `.title()` pone en mayúscula la primera letra de cada palabra. El `while` impide que el nombre quede vacío.
```python
# Req. 1: Identificación del usuario. La funcion se hace en un ciclo while para evitar campo en blanco
def pedir_nombre():
    nombre = input("Ingresa tu nombre: ").strip().title()
    while nombre == "":
        nombre = input("El nombre no puede quedar vacio. Ingresa tu nombre: ").strip().title()
    return nombre
```

6. `mostrar_bienvenida` genera el mensaje de bienvenida con operadores de cadenas (Req. 2): `*` repite el símbolo `=` para formar la línea decorativa y `+` une el nombre del cajero con el resto del mensaje.
```python
# Req. 2: Función de bienvenida usando operadores de cadenas.
def mostrar_bienvenida(cajero):
    linea = "=" * 55
    mensaje = "Bienvenido(a), " + cajero + ". Tu turno como cajero ha iniciado."
    print("\n" + linea)
    print(mensaje)
    print("Sistema de caja - Minisuper | El Puy")
    print(linea)
```

7. `pantalla_de_carga` recorre con un `for` la lista `pasos` (Req. 3). En cada vuelta construye la barra de progreso con `#` para el avance y `-` para lo faltante, calcula el porcentaje con división entera `//` y espera 1 segundo con `time.sleep()`, lo que da un total de 5 segundos.
```python
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
```

8. `pedir_fecha` solicita la fecha de operación (Req. 6). Con `.replace()` convierte los guiones y espacios en `/`, y con `.split("/")` separa el texto en una lista. Después valida que existan tres partes, que sean números (`except ValueError`) y que el día, el mes y el año estén dentro de rango; si algo falla, `continue` regresa al inicio del ciclo. Con la fecha válida, empaqueta la tupla `fecha = dd, mm, aaaa` y la regresa.
```python
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
```

### Menú e inactividad
9. `mostrar_menu` recorre la matriz `MENU` con un `for` e imprime la clave (`fila[0]`) y el nombre (`fila[1]`) de cada opción (Req. 4). Debajo muestra el cajero y la fecha activos.
```python
# Funcion que recorre la matriz para mostrar las opciones
def mostrar_menu(cajero, fecha):
    print("\n+-+---------------------------")
    for fila in MENU:
        print("|" + fila[0] + "| " + fila[1])
    print("+-+---------------------------\n")
    print("Cajero: " + cajero + "  |  Fecha: " + fecha_a_texto(fecha))
```

10. `buscar_opcion` recorre la matriz y regresa la fila cuya clave coincide con la opción escrita. Si no la encuentra, regresa `None`, lo que permite identificar una opción inexistente.
```python
# La seleccion tambien se hace recorriendo la matriz mediante una funcion que regresa valor, así
# podemos identificiar si se encontró la opcion
def buscar_opcion(opcion):
    for fila in MENU:
        if fila[0] == opcion:
            return fila
    return None
```

11. `contar_inactividad` se ejecuta en un hilo aparte mientras el menú espera una respuesta (Req. 5). Su `for` da una vuelta por segundo; en cada una revisa el diccionario compartido `estado` y, si el usuario ya respondió, termina con `return`. Si el `for` completa todas sus vueltas, significa que pasaron 10 minutos sin actividad: marca `estado["inactivo"] = True` y muestra el aviso de suspensión.
```python
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
```

### Manejo de archivos
12. `guardar_en_archivo` concentra la escritura de todos los reportes (Req. 7 y 8). Abre el archivo en modo `"a"`, que agrega la información al final sin borrar lo anterior. En cada registro escribe primero la fecha de la tupla (Req. 6), luego cada línea recibida con un `for` y al final un separador. Los errores de permisos (`PermissionError`) y cualquier otro fallo del sistema al escribir (`OSError`) se controlan con mensajes.
13. Se agrega `encoding="utf-8"` para que los caracteres especiales, como la ñ o los acentos, se guarden y se lean siempre de la misma forma, sin importar la computadora donde se ejecute el programa. Sin este parámetro, Python usa la codificación predeterminada del sistema operativo, que en Windows suele ser distinta a UTF-8; esto puede provocar caracteres raros, por ejemplo al escribir un apellido como "Peña", o un `UnicodeDecodeError` al leer el archivo. Por esa razón se usa tanto al escribir como al leer los reportes.
```python
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
```

14. `ver_reportes` muestra los archivos disponibles recorriendo el diccionario `REPORTES` y pide el nombre del que se desea abrir (Req. 7). El nombre se normaliza con `.strip().lower()` y, si no termina en `.txt` (`.endswith()`), se le agrega la extensión.
15. El archivo se abre en modo `"r"` con `encoding="utf-8"` y su contenido se lee con `.read()`; si está vacío, se muestra un aviso. Los errores se controlan con `FileNotFoundError` (archivo inexistente o nombre mal escrito), `PermissionError`, `UnicodeDecodeError` (archivo que no se puede leer como texto) y `OSError` para cualquier otro fallo (Req. 8).
```python
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
```

### Opciones del menú
16. `registrar_venta` conserva la lógica del prototipo: un `while True` pide el precio de cada producto hasta que se digita 0 (`break`). Los precios negativos y las cantidades menores a 1 se rechazan con `continue`. Por cada producto se calcula su subtotal y se acumulan el subtotal de la venta y el número de artículos.
```python
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
```

17. Si no se agregó ningún producto, la venta se cancela con `return`. En caso contrario se aplican los descuentos del prototipo (10% arriba de $500 y 5% arriba de $200) y se muestra el total antes de cobrar.
```python
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
```

18. El método de pago se repite con `while metodo == ""` hasta recibir una opción válida. En efectivo se pide el monto que entrega el cliente; mientras no alcance, se muestra lo que falta y se vuelve a pedir. El cambio se obtiene con una resta.
```python
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
```

19. Se actualizan los acumulados del diccionario `turno`, separando el total en efectivo o tarjeta, y el número de transacción se usa como folio. Después se imprime el ticket.
```python
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
```

20. Se arma una lista con los datos de la venta y se guarda en `reporte_ventas.txt`. Luego se arma otra lista para `reporte_metodos_pago.txt`, a la que se agregan con `.append()` el monto recibido y el cambio cuando el pago es en efectivo.
```python
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
```

21. `registrar_devolucion` pide el producto (sin permitir que quede vacío), el monto (mayor a 0) y el motivo (si se omite, queda como "Sin especificar"). El producto y el motivo son solo informativos; el monto es el único dato que afecta los totales, ya que se suma a `turno["devoluciones"]`. También se incrementa el contador de devoluciones y el registro se guarda en `reporte_devoluciones.txt`.
```python
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
```

22. `corte_de_caja` calcula el total neto (ventas menos devoluciones) y reúne los datos del turno en la lista `lineas`. Esa misma lista se imprime con un `for` y se guarda en `corte_caja.txt`, por lo que lo mostrado en pantalla y lo guardado en el archivo siempre coinciden.
```python
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
```

### Programa principal
23. Creamos el diccionario `turno` con los acumulados del turno. Como los diccionarios son mutables, las funciones pueden modificarlos directamente sin usar variables globales.
```python
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
```

24. El ciclo `while programa_activo` representa la pantalla de inicio: pide el nombre, muestra la bienvenida, la pantalla de carga y solicita la fecha. Cuando se regresa a esta pantalla por inactividad, el diccionario `turno` no se reinicia.
```python
programa_activo = True
while programa_activo:

    # ---------- Pantalla de inicio ----------
    print("\n=== Sistema de caja - Minisuper | El Puy ===")
    cajero = pedir_nombre()
    mostrar_bienvenida(cajero)
    pantalla_de_carga()
    fecha = pedir_fecha()
    print("Fecha registrada: " + fecha_a_texto(fecha))
```

25. El ciclo `while en_menu` muestra el menú y crea un diccionario `estado` nuevo en cada vuelta. Con `threading.Thread` se inicia el hilo que ejecuta `contar_inactividad`, recibiendo `estado` en la tupla `args=(estado,)`. `daemon = True` hace que el hilo se detenga si el programa termina. En cuanto el usuario responde el `input()`, se marca `estado["respondio"] = True` para detener el conteo.
```python
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
```

26. Si el contador marcó inactividad, lo escrito se interpreta como la respuesta a la pregunta de continuar. Se normaliza con `.title()` y se repite hasta recibir "Si" o "No". Con "No", `en_menu` pasa a `False` y el programa regresa a la pantalla de inicio; con "Si", `continue` vuelve a mostrar el menú.
```python
        if estado["inactivo"]:
            respuesta = opcion.title()
            while respuesta != "Si" and respuesta != "No":
                respuesta = input("Por favor, indica \"si\"/\"no\" ").strip().title()

            if respuesta == "No":
                print("\nRegresando a la pantalla de inicio...")
                en_menu = False
            continue   # Con "Si" se vuelve a mostrar el menu
```

27. Con `buscar_opcion` se localiza la opción dentro de la matriz; si regresa `None`, se avisa que la opción no es válida. Con la clave de la fila se llama a la función correspondiente. La opción 5 muestra el resumen del turno y cambia ambas banderas a `False`, lo que termina los dos ciclos y cierra el sistema.
```python
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
```
---

### Depuración técnica con PDB (Req. 9)

Comandos utilizados durante la depuración:

| Comando | Función |
| --- | --- |
| `b número` | Coloca un breakpoint en esa línea |
| `b función` | Coloca un breakpoint al inicio de esa función |
| `c` | Continúa la ejecución hasta el siguiente breakpoint |
| `n` | Ejecuta la línea actual y se detiene en la siguiente |
| `p expresión` | Muestra el valor de una variable o expresión |
| `cl número` | Elimina un breakpoint |
| `q` | Termina la depuración |

Durante el desarrollo del programa se localizaron con PDB cuatro fallas de lógica de control. Cada falla se corrigió antes de continuar con la siguiente, por lo que cada sesión de depuración se realizó con las fallas anteriores ya corregidas. En cada caso se muestra el código con la falla, la sesión de depuración y el código corregido, que es el que forma parte de la versión final. En las transcripciones, `...` indica partes de la salida que se omitieron por no ser relevantes.

#### Caso 1: el menú solo reconocía la opción 1
Código con la falla:
```python
def buscar_opcion(opcion):
    for fila in MENU:
        if fila[0] == opcion:
            return fila
        return None
```
Al elegir cualquier opción distinta de 1, incluida la 5 (Salir), el programa mostraba "Opcion invalida". Colocamos un breakpoint en la función `buscar_opcion` con `b buscar_opcion` y avanzamos línea por línea con `n`. En la primera vuelta del `for`, la fila revisada era la de la opción 1, la comparación resultó `False` y el programa ejecutó `return None` de inmediato, sin revisar las demás filas. El `return None` estaba indentado dentro del `for`, por lo que la función terminaba siempre en la primera vuelta.
```text
(Pdb) b buscar_opcion
Breakpoint 1 at proyecto_final.py:134
(Pdb) c
...
Elige una opcion (1-5): 3
> proyecto_final.py(135)buscar_opcion()
-> for fila in MENU:
(Pdb) p opcion
'3'
(Pdb) n
> proyecto_final.py(136)buscar_opcion()
-> if fila[0] == opcion:
(Pdb) n
> proyecto_final.py(138)buscar_opcion()
-> return None
(Pdb) p fila
['1', 'Registrar venta']
(Pdb) p fila[0] == opcion
False
(Pdb) n
--Return--
> proyecto_final.py(138)buscar_opcion()->None
-> return None
(Pdb) n
> proyecto_final.py(422)<module>()
-> if fila is None:
(Pdb) n
> proyecto_final.py(423)<module>()
-> print("Opcion invalida, intenta de nuevo.")
(Pdb) cl 1
Deleted breakpoint 1 at proyecto_final.py:134
(Pdb) c
Opcion invalida, intenta de nuevo.
...
Elige una opcion (1-5): 5
Opcion invalida, intenta de nuevo.
```
**Corrección:** se movió `return None` fuera del `for`, para que solo se ejecute después de revisar todas las filas de la matriz.
```python
def buscar_opcion(opcion):
    for fila in MENU:
        if fila[0] == opcion:
            return fila
    return None
```

#### Caso 2: las compras mayores a $500 recibían el descuento de 5%
Código con la falla:
```python
    if subtotal_venta > 200:
        descuento = subtotal_venta * 0.05
    elif subtotal_venta > 500:
        descuento = subtotal_venta * 0.10
    else:
        descuento = 0.0
```
Una compra de $600 debía recibir el 10% de descuento ($60), pero recibía $30. Colocamos un breakpoint en la línea 244, donde inician las condiciones del descuento, y avanzamos con `n`. Como $600 también es mayor a $200, la primera condición se cumplía y el programa entraba al bloque del 5%; al cumplirse una condición, el `elif` ya no se evalúa, por lo que el descuento de 10% nunca se aplicaba.
```text
(Pdb) b 244
Breakpoint 1 at proyecto_final.py:244
(Pdb) c
...
Precio unitario del producto ($): 600
Cantidad comprada: 1
-> Subtotal parcial de este producto: $600.00

Precio unitario del producto ($): 0
> proyecto_final.py(244)registrar_venta()
-> if subtotal_venta > 200:
(Pdb) p subtotal_venta
600.0
(Pdb) p subtotal_venta > 200
True
(Pdb) n
> proyecto_final.py(245)registrar_venta()
-> descuento = subtotal_venta * 0.05
(Pdb) n
> proyecto_final.py(251)registrar_venta()
-> total_venta = subtotal_venta - descuento
(Pdb) p descuento
30.0
(Pdb) p subtotal_venta > 500
True
(Pdb) cl 1
Deleted breakpoint 1 at proyecto_final.py:244
(Pdb) c

Subtotal general: $600.00
Descuento aplicado: $30.00
Total a cobrar: $570.00
```
**Corrección:** se invirtió el orden de las condiciones para evaluar primero la más restrictiva (mayor a $500) y después la de mayor a $200.
```python
    if subtotal_venta > 500:
        descuento = subtotal_venta * 0.10
    elif subtotal_venta > 200:
        descuento = subtotal_venta * 0.05
    else:
        descuento = 0.0
```

#### Caso 3: un pago insuficiente se aceptaba en el segundo intento
Código con la falla:
```python
    pago_cliente = total_venta
    cambio = 0.0
    if metodo == "Efectivo":
        pago_cliente = pedir_decimal("Monto con el que paga el cliente ($): ")
        if pago_cliente < total_venta:
            faltante = total_venta - pago_cliente
            print(f"El monto no alcanza, faltan ${faltante:.2f}")
            pago_cliente = pedir_decimal("Monto con el que paga el cliente ($): ")
        cambio = pago_cliente - total_venta
```
En una venta de $100 pagada en efectivo, el primer pago de $50 se rechazaba, pero un segundo pago de $60 se aceptaba y el ticket mostraba un cambio negativo. Colocamos un breakpoint en la línea 277, donde se calcula el cambio, y consultamos los valores: el pago seguía siendo menor al total (`True`) y aun así el programa continuó, dejando el cambio en -40. La validación usaba `if`, que solo revisa la condición una vez.
```text
(Pdb) b 277
Breakpoint 1 at proyecto_final.py:277
(Pdb) c
...
Total a cobrar: $100.00

Metodo de pago:  1. Efectivo   2. Tarjeta
Elige el metodo de pago (1-2): 1
Monto con el que paga el cliente ($): 50
El monto no alcanza, faltan $50.00
Monto con el que paga el cliente ($): 60
> proyecto_final.py(277)registrar_venta()
-> cambio = pago_cliente - total_venta
(Pdb) p total_venta, pago_cliente
(100.0, 60.0)
(Pdb) p pago_cliente < total_venta
True
(Pdb) n
> proyecto_final.py(280)registrar_venta()
-> turno["transacciones"] += 1
(Pdb) p cambio
-40.0
(Pdb) cl 1
Deleted breakpoint 1 at proyecto_final.py:277
(Pdb) c

=================================
--- Ticket de Venta ---
Folio: 1
Subtotal general: $100.00
Descuento aplicado: $0.00
Total a cobrar: $100.00
Metodo de pago: Efectivo
Recibido: $60.00
Cambio a entregar: $-40.00
```
**Corrección:** se cambió el `if` por un `while`, que vuelve a pedir el monto las veces necesarias hasta que el pago cubra el total.
```python
    pago_cliente = total_venta
    cambio = 0.0
    if metodo == "Efectivo":
        pago_cliente = pedir_decimal("Monto con el que paga el cliente ($): ")
        while pago_cliente < total_venta:
            faltante = total_venta - pago_cliente
            print(f"El monto no alcanza, faltan ${faltante:.2f}")
            pago_cliente = pedir_decimal("Monto con el que paga el cliente ($): ")
        cambio = pago_cliente - total_venta
```

#### Caso 4: las devoluciones no se sumaban a los acumulados del turno
Código con la falla:
```python
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

    print(f"Devolucion registrada: ${monto:.2f}")
```
Después de registrar una devolución de $25, el corte de caja mostraba 0 devoluciones y $0.00 devueltos. Colocamos un breakpoint en la línea 340, al final de `registrar_devolucion`, y consultamos el diccionario `turno`: tanto `turno["devoluciones"]` como `turno["num_devoluciones"]` seguían en 0, porque la función capturaba el monto pero nunca lo sumaba a los acumulados.
```text
(Pdb) b 340
Breakpoint 1 at proyecto_final.py:340
(Pdb) c
...
--- Registrar Devolucion ---
Producto devuelto: Leche
Monto a devolver ($): 25
Motivo de la devolucion: Caducada
> proyecto_final.py(340)registrar_devolucion()
-> print(f"Devolucion registrada: ${monto:.2f}")
(Pdb) p monto
25.0
(Pdb) p turno["devoluciones"], turno["num_devoluciones"]
(0.0, 0)
(Pdb) cl 1
Deleted breakpoint 1 at proyecto_final.py:340
(Pdb) c
Devolucion registrada: $25.00

Registro guardado en reporte_devoluciones.txt

...
Elige una opcion (1-5): 3

--- Corte de Caja ---
Fecha: 24/09/2026
Cajero: Ana Lopez
Ventas registradas: 0
Ventas en efectivo: $0.00
Ventas con tarjeta: $0.00
Total vendido: $0.00
Devoluciones: 0
Total devuelto: $0.00
Total neto del turno: $0.00
```
Por la misma causa, el registro en `reporte_devoluciones.txt` se guardaba con el número de devolución en 0:
```text
Fecha de operacion: 24/09/2026
Devolucion No.: 0
Cajero: Ana Lopez
Producto: Leche
Monto devuelto: $25.00
Motivo: Caducada
----------------------------------------
```
**Corrección:** se agregó el acumulador, que suma el monto a `turno["devoluciones"]` e incrementa `turno["num_devoluciones"]`. Con esto, el corte de caja descuenta las devoluciones del total neto y cada registro guarda su número correcto.
```python
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
```
---
