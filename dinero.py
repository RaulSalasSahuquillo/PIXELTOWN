from ciudad.ciudad import Ciudad
import time # Necesario para la pausa

def dinero_ciudadanos():
    dinerototal = 100000
    ciudad = Ciudad()
    poblacion_anterior = ciudad.poblacion

    while True:
        if ciudad.poblacion > poblacion_anterior:
            nuevos_habitantes = ciudad.poblacion - poblacion_anterior
            dinerototal = dinerototal + nuevos_habitantes * 10000
            print(f"Población aumentó a {ciudad.poblacion}. Dinero total ahora: {dinerototal}")
            poblacion_anterior = ciudad.poblacion
        time.sleep(1)