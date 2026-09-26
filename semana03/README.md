# Semana 3 - Avance de reto/proyecto (FASE I)

## Reporte de avance:

## 1. Análisis Organizacional
La organización seleccionada es Minisuper “El Puy”, un negocio local que atiende a clientes de la colonia donde se ubica. El área de impacto identificada es el punto de venta, específicamente la caja registradora, donde el cajero recibe cada compra, calcula el monto a cobrar y, al cierre del turno, debe reportar el total vendido y el número de ventas realizadas.

Actualmente este proceso se realiza a mano: el cajero utiliza una calculadora para sumar el precio de los productos, aplica de memoria los descuentos que la tienda ofrece a partir de cierto monto de compra, y anota en un cuaderno el resultado de cada venta para obtener el total al final del día. Esta forma de trabajo es propensa a errores de cálculo, aplicación inconsistente de los descuentos y pérdida de tiempo al cerrar el turno mientras suma a mano las ventas.

## 2. Definición del Problema
Problema: la tienda no cuenta con una herramienta que calcule de forma automática el total de cada venta, aplique los descuentos vigentes de manera consistente y mantenga un control acumulado de las ventas del turno. Esto aunado a la creciente clientela con el paso de los años genera la necesidad de este programa.

**Reglas de negocio:**

- Cada venta captura el precio unitario y la cantidad comprada de multiples productos.
- El subtotal de la venta es el resultado de multiplicar el precio unitario por la cantidad comprada.
- Si el subtotal de la venta es mayor a $500.00, se aplica un descuento del 10%.
- Si el subtotal se encuentra entre $200.01 y $500.00, se aplica un descuento del 5%.
- Si el subtotal es de $200.00 o menor, no se aplica ningún descuento.
- El turno de caja permanece abierto hasta que el cajero elige cerrarlo desde el menú principal.
- Al cerrar el turno, el sistema reporta el total acumulado de ventas y el número de transacciones realizadas.

## 3. Listado de Requerimientos
- Debe presentar un menú con las opciones de registrar venta, consultar corte de caja y salir.
- Debe permitir registrar una venta con multiples articulos y precios distintos, capturando el precio unitario y la cantidad del producto por separado.
- Debe calcular automáticamente el subtotal de cada venta.
- Debe aplicar el porcentaje de descuento que corresponda según el monto del subtotal.
- Debe desglosar el monto parcial de los articulos registrados y el descuento que se le otorga por la venta total.
- Debe acumular el total de ventas realizadas durante el turno.
- Debe contar el número de transacciones registradas en el turno.
- Debe mostrar un resumen del corte de caja con el total vendido y el número de ventas al finalizar el turno.
- Debe validar que la opción capturada en el menú corresponda a una de las opciones disponibles, de lo contrario, volver a solicitar capturar.

## 4. Clasificación de Datos

|Variable|Tipo de dato|Descripción|
|--------|------------|-----------|
|total_ventas |Número real con decimal (float) |Acumulado total del dinero vendido durante todo el turno.|
|numero_transacciones |Número entero (int) |Contador del número total de ventas o tickets registrados.|
|continuar |Booleano (bool) |Bandera que controla si el ciclo principal del menú sigue activo.|
|opcion |Cadena de texto (str) |Opción del menú ingresada por el usuario.|
|subtotal_venta |Número real con decimal (float) |Suma acumulada de los productos ingresados en la venta actual.|
|precio_unitario |Número real con decimal (float) |Precio por unidad del producto capturado por el cajero.|
|cantidad |Número entero (int) |Número de unidades compradas del producto actual.|
|subtotal_producto |Número real con decimal (float) |Resultado de multiplicar el precio unitario por la cantidad del producto actual.|
|descuento |Número real con decimal (float) |Monto de descuento calculado según las reglas de negocio sobre el subtotal general.|
|total_venta |Número real con decimal (float) |Monto final a cobrar de la venta actual (subtotal menos descuento).|

## 5. Operadores del Lenguaje

|Operador|Tipo|Justificación / Uso en el código|
|--------|----|--------------------------------|
|* |Matemático (Aritmético) |Multiplica el `precio_unitario` por la `cantidad` para obtener el subtotal de cada producto individual.|
|+= |Matemático (Asignación compuesta) |Suma y acumula de forma abreviada el `subtotal_producto` dentro del `subtotal_venta` general.|
|- |Matemático (Aritmético) |Resta el monto del `descuento` al `subtotal_venta` para obtener el `total_venta` final a cobrar.|
|+ |Matemático (Aritmético) |Suma el `total_venta` al acumulador `total_ventas` del turno, e incrementa en `1` el contador `numero_transacciones`.|
|== |Relacional (Comparación) |Verifica si el `precio_unitario` ingresado es exactamente igual a `0` para activar la condición de salida (`break`) del ciclo de venta.|
|> |Relacional (Comparación) |Evalúa si el `subtotal_venta` es mayor a `500` o `200` para determinar qué porcentaje de descuento aplicar según las reglas de negocio.|

## 6. Estructuras de Control

### 1. Estructuras Iterativas (Ciclos / Loops)
- Ciclo while continuar: (Bucle principal del menú): Mantiene el sistema de caja abierto de forma continua, repitiendo el menú principal hasta que el usuario decida salir seleccionando la opción 3 (lo que cambia continuar a False o ejecuta un break).

- Ciclo while True: (Bucle interno de venta de productos): Permite capturar de forma repetida múltiples artículos y cantidades para una misma venta. Se ejecuta indefinidamente hasta que se cumple la condición de salida (break).

### 2. Estructuras Condicionales (Tomas de decisión)
- Condicional `if - elif - else` (Menú principal): Evalúa el valor de la variable opcion ingresada por el usuario para decidir qué bloque de código ejecutar:

    - `opcion == "1"`: Inicia el proceso de registro de múltiples productos y cálculo de la venta.

    - `opcion == "2"`: Muestra el corte de caja parcial (transacciones y total acumulado).

    - `opcion == "3"`: Cierra el turno y finaliza el programa mediante un break.

    - `else`: Captura entradas inválidas y muestra un mensaje de error.

- Condicional `if` (Condición de salida del ciclo interno): Evalúa si `precio_unitario == 0` para activar la instrucción `break` y terminar la captura de productos de la venta actual.

- Condicional `if - elif - else` (Reglas de descuento): Evalúa el valor de `subtotal_venta` mediante operadores relacionales para determinar el porcentaje de descuento aplicable:

    - Si es mayor a 500: Aplica un 10% de descuento.

    - Si es mayor a 200 (y menor o igual a 500): Aplica un 5% de descuento.

    - `else`: No aplica ningún descuento (0.0).

## 7. Diseño Algorítmico
Se adjunta diagrama de flujo en PSeInt

![alt text](Minisuper_El_Puy.png)

