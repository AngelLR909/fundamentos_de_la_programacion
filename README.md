# Actividad 1
## Descripcion del reto
### Calculadora de Tiempo Digital

Debemos realizar una calculadora que registre el tiempo diario que una persona pasa en plataformas digitales. Con los datos capturados y procesados, se deberá mostrar un resumen ordenado de los resultados.

## Requerimientos
1. Se debe solicitar nombre de usuario mediante la función `input()`.
2. Solicitar tiempo dedicado a almenos 5 plataformas digitales.
3. Emplear la función `float()` para poder ingresar valores decimales.
4. Calcular la suma del tiempo total diario invertido en actividades digitales.
5. Debemos calcular el porcentaje del día utilizado en actividades digitales con la función `porcentaje = (tiempo_total / 24) * 100`
6. Mostrar en pantalla "Nombre de usuario", "Tiempo acumulado", "Porcentaje calculado"

## Proceso

1. Usuario ingresa los datos solicitados

```python
username = input("Por favor, ingresa tu nombre: ")
print("\nA continuación, ingresa el tiempo en horas:")

videojuegos = float(input("Videojuegos: "))
redes_sociales = float(input("Redes sociales (FB, IG, X, TikTok): "))
streaming = float(input("Plataformas de Streaming(Netflix, HBOMAX, Disney+, YT, PrimeVideo, etc.): "))
compras_online = float(input("Compras en línea (Apps como Amazon/Mercado Libre, Shein, AliExpress, etc): "))
trabajo_estudio_en_linea = float(input("Estudio o trabajo EN LÍNEA: "))
```

2. Se calcula la suma de los tiempos registrados y se calcula el porcentaje del día

```python
tiempo_total = (
    videojuegos
    +redes_sociales
    +streaming
    +compras_online
    +trabajo_estudio_en_linea
)

porcentaje_dia = (tiempo_total / 24) * 100
```

3. Se muestran el resumen de los resultados, considerando adicionalmente si, el resultado no pasa de las 24 hrs y si no son negativas. Se insertan las variables con f-string para el resumen y `:.2f` para mostrar dos decimales.

```python
print("\n         RESUMEN DE USO DIGITAL DIARIO           ")
print(f"\nUsuario: {username}")
print(f"Tiempo total acumulado: {tiempo_total:.2f}")
print(f"Porcentaje del día usado: {porcentaje_dia:.2f}%")

if tiempo_total > 24:
    print("\nNo puedes exceder las 24 hrs")

elif tiempo_total < 0:
    print ("\nNo puedes tener menos de 0 hrs")

else:
    print(f"\nTu tiempo total es {tiempo_total:.2f} hrs")
```

A continuación se adjunta evidencia de la salida de ejecución del código:

![Evidencia Calculadora](./assets/evidencias/calculadora_ss.png)

## EXTRA 1
### DIVISION DE CUENTA CON PROPINA

El programa pide el total de la cuenta de un restaurante, porcentaje de propina y el número de personas que pagarán:

```python
total = float(input("\nIngrese el total de la cuenta: "))
propina = float(input("¿Qué porcentaje de propina te gustaría dejar?: "))
total_personas = float(input("¿Cuántas personas pagarán?"))
```

Después, en base a los datos capturados, asigna el valor total de la propina, cuanto pagarán con la propina incluida (calculada previamente) y la división de la cuenta total con propina.

```python
monto_propina = total * (propina / 100)
total_con_propina = total + monto_propina
monto_por_persona = total_con_propina / total_personas
```

Finalmente, se muestran los resultados, insertando los valores con f-string y añadiendo `:.2f` para mostrar valores con 2 decimales.

```python
print(f"\nTotal de propina: {monto_propina:.2f}")
print(f"Cuenta total: {total_con_propina:.2f}")
print(f"Pago por persona: {monto_por_persona:.2f}")
print("\n           GRACIAS POR SU COMPRA           ")
```

Se adjunta evidencia de la ejecución del código:
![EvidenciaExtra1](./assets/evidencias/extra1.png)

## EXTRA 2
### CONVERSOR DE MINUTOS A DIAS, HRS Y MINUTOS

El programa pide la cantidad total de minutos

```python
print("         CONVERSOR MINUTOS A DÍAS, HRS Y MINUTOS            \n")

total_minutos = int(input("Total de minutos: "))
```

Definimos las equivalencias para conversión y calculamos para la conversión
Utilizamos la división entera (//) para calcular cuántos días completos caben dentro de total_minutos
(%) obtiene los minutos que sobran después de separar los días completos.

```python
minutosxdia = 1440
minutosxhora = 60

dias = total_minutos // minutosxdia

minutos_restantes_dias = total_minutos % minutosxdia

horas = minutos_restantes_dias // minutosxhora

minutos_finales = minutos_restantes_dias % minutosxhora
```

Finalmente mostramos los resultados, f-string para insertar nuestros valores

```python
print(f"{total_minutos} minutos = {dias} día(s), {horas} hora(s), {minutos_finales} minuto(s)")
```
A continuación se muestra evidencia de la ejecución exitosa del código:

![EvidenciaExtra2](./assets/evidencias/extra2.png)

## EXTRA 3
### CALIFICACIÓN FINAL PONDERADA

Se ingresan las calificaciones obtenidas en cada parcial, se usa función float para decimales.

```python
print("         CALIFICACIÓN FINAL            \n")

parcial1 = float(input("Parcial 1 (30%): "))
parcial2 = float(input("Parcial 2 (30%): "))
parcial3 = float(input("Parcial 3 (40%): "))
```

Se asigna ponderación a los parciales. Multiplicamos la calificación ingresada por el usuario por la ponderación asignada y hacemos la suma de los valores.

```python
nota_p1 = parcial1 * 0.30
nota_p2 = parcial2 * 0.30
nota_p3 = parcial3 * 0.40

calificacion_final = (
    nota_p1 
    +nota_p2 
    +nota_p3
)
```

Para finalizar, usamos f-string para insertar nuestro valor y `:.2f` para mostrar solo dos decimales. 

```python
print(f"Tu calificación final es: {calificacion_final:.2f}")
```
Se adjunta una imágen de evidencia a continuación:

![EvidenciaExtra3](./assets/evidencias/extra3.png)

## EXTRA 4
### CONVERSOR DE MONEDA

Nuestro programa pide la cantidad de MXN que deseas convertir. Posteriormente nos solicita asignar el valor al cambio de USD y EUR respectivamente.

```python
print("         CONVERSOR DE MONEDAS            \n")

mxn = float(input("Cantidad en MXN: "))
usd = float(input("Tipo de cambio USD: "))
eur = float(input("Tipo de cambio EUR: "))
```

Realizamos la conversión dividiendo la cantidad de MXN que vamos a convertir entre el cambio, USD o EUR respectivamente, asignados previamente. 

```python
dolares = mxn / usd
euros = mxn / eur
```

Para finalizar, mostramos nuestras equivalencias, igualmente usando f-string y `:.2f` para redondear a dos decimales. 

```python
print(f"\n${mxn:.2f} MXN equivalen a:")
print(f"USD: {dolares:.2f}")
print(f"EUR: {euros:.2f}")
```

Se adjunta evidencia de la ejecución del código:

![EvidenciaExtra4](./assets/evidencias/extra4.png)