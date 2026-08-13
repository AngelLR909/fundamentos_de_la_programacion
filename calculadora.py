#entrada de datos por el usuario mediante input
username = input("Por favor, ingresa tu nombre: ")
print("\nA continuación, ingresa el tiempo en horas:")

videojuegos = float(input("Videojuegos: "))
redes_sociales = float(input("Redes sociales (FB, IG, X, TikTok): "))
streaming = float(input("Plataformas de Streaming(Netflix, HBOMAX, Disney+, YT, PrimeVideo, etc.): "))
compras_online = float(input("Compras en línea (Apps como Amazon/Mercado Libre, Shein, AliExpress, etc): "))
trabajo_estudio_en_linea = float(input("Estudio o trabajo EN LÍNEA: "))

#calculos de tiempo
tiempo_total = (
    videojuegos
    +redes_sociales
    +streaming
    +compras_online
    +trabajo_estudio_en_linea
)

porcentaje_dia = (tiempo_total / 24) * 100

#print de resultados
print("\n         RESUMEN DE USO DIGITAL DIARIO           ")
print(f"\nUsuario: {username}")
print(f"Tiempo total acumulado: {tiempo_total}")
print(f"Porcentaje del día usado: {porcentaje_dia}%")

if tiempo_total > 24:
    print("\nNo puedes exceder las 24 hrs")

elif tiempo_total < 0:
    print ("\nNo puedes tener menos de 0 hrs")

else:
    print(f"\nTu tiempo total es {tiempo_total} hrs")