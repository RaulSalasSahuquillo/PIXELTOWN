# PIXELTOWN - ARCHIVO PRINCIPAL DEL JUEGO
# Este archivo contiene el bucle principal y la lógica para ejecutar el juego.

# --- IMPORTACIÓN DE LIBRERÍAS Y MÓDULOS ---
import pygame
import time
import sys
from ciudad.ciudad import Ciudad
from texto import titulo
from mapa import mostrar_mapaascii
from mapa import mostrar_mapagrafico
from bloquegrafico import rio
from bloquegrafico import edificio1

# --- FUNCIÓN PRINCIPAL (main) ---
def main():
    # Inicializa todos los módulos de Pygame para su uso.
    pygame.init()
    # Carga y reproduce la música de fondo en un bucle infinito.
    pygame.mixer.music.load("anewbegining.mp3")
    pygame.mixer.music.play(-1) # El -1 hace que la música se repita indefinidamente
    
    # Muestra el título del juego y solicita datos iniciales al jugador.
    titulo()
    print("¡Bienvenido a PixelTown!")
    tu_nombre = input("¿Cómo te llamas? ")
    nombre_ciudad = input("¿Cómo quieres llamar a tu ciudad? ")

    print("¡Empieza la gestión de tu ciudad!")
    # Bucle para que el jugador elija el tipo de mapa.
    while True:
        tipo_mapa = int(input("Elige el tipo de mapa:\n1. Mapa gráfico\n2. Mapa ASCII\n3. Preview de los mapas\n"))
        if tipo_mapa == 1: # Mapa en desarrollo
            print("\nHas elegido un mapa grafico.")
            break
        elif tipo_mapa == 2: # Todavía no programado. Posible eliminación
            print("\nHas elegido un mapa en ASCII.") 
            break
        elif tipo_mapa == 3:
            print("\nAquí puedes ver una vista previa de los mapas.\n MAPA EN ASCII:")
            mostrar_mapaascii()
            print("\n MAPA GRÁFICO:")
            mostrar_mapagrafico()
                    
    # --- LÓGICA PRINCIPAL PARA EL MAPA GRÁFICO ---
    if tipo_mapa == 1:
        print(f"Bienvenido a la ciudad de {nombre_ciudad}, {tu_nombre}!\n")
        # Crea una instancia de la clase Ciudad con el nombre proporcionado.
        ciudad = Ciudad(nombre_ciudad)
        ciudad.mostrar_estado()
        print("Cargando datos iniciales del mapa...")
        rio()
        # Bucle principal de acciones del juego. NOTA: Actualmente, este bucle se rompe después de la primera acción.
        while True:
            accion = input("Escribe la acción que deseas realizar: \nConstruir\nAlimentar\nFacturar\n")
            # Limpia la entrada del usuario para que no sea sensible a mayúsculas/minúsculas o espacios.
            accion_limpia = accion.strip().lower()
            if accion_limpia == "construir":
                print("Has elegido construir un edificio.")
                break
            elif accion_limpia == "alimentar": # Todavía no definida
                print("Has elegido alimentar a la población.")
                break
            elif accion_limpia == "facturar": # Todavía no definida
                print("Has elegido facturar a los ciudadanos.")
                break
            else:
                print("Acción no reconocida. Vuelve a intentarlo.\n")
        
        # --- LÓGICA DE CONSTRUCCIÓN ---
        # Verifica si la acción elegida fue 'construir'.
        if accion_limpia == "construir":
            nombre_edificio = input("¿Qué edificio quieres construir?\n 1. Casa\n 2. Escuela\n 3. Hospital\n 4. Piso\n") # Escuela, hospital y piso todavía no definidos
            if nombre_edificio == "1": # CASA
                # Muestra al jugador los detalles de la construcción antes de confirmar.
                print(f"Información sobre la casa:\nCosto: 1000\nEdificios totales: {ciudad.edificios + 1}\nDinero restante: {ciudad.dinero - 1000}\nFelicidad: {ciudad.felicidad + 5}%\nExperiencia: {ciudad.experiencia + 10}")
                confirmacion = input("¿Quieres continuar con la compra? Escribe [CONFIRMAR] si es así.\nEscribe [CANCELAR] para cancelar.\n")
                if confirmacion.upper() == "CONFIRMAR": # Usar .upper() para aceptar "confirmar", "Confirmar", etc.
                    print("Construyendo edificio...")
                    pygame.init()
                    pygame.mixer.music.load("efectoconstruccion.mp3")
                    pygame.mixer.music.play() 
                    time.sleep(8)
                    edificio1()
                    rio()
                    # Si el jugador confirma, se actualiza el estado de la ciudad.
                    print("Edificio construido.")
                    ciudad.edificios = ciudad.edificios + 1
                    ciudad.dinero = ciudad.dinero - 1000
                    ciudad.felicidad = ciudad.felicidad + 5
                    ciudad.experiencia = ciudad.experiencia + 10
                    ciudad.mostrar_estado()
                if confirmacion.upper() == "CANCELAR":
                    # Penalización a la felicidad si el jugador cancela la construcción.
                    print(f"Compra cancelada. ¡La felicidad de la población ha disminuido un 5%! Actualmente es: {ciudad.felicidad - 5}%")
                    ciudad.felicidad = ciudad.felicidad - 5
                    ciudad.mostrar_estado()
            elif nombre_edificio == "2": # ESCUELA
                # Comprueba si el jugador tiene la experiencia necesaria para construir.
                if ciudad.experiencia < 100:
                    print("No tienes suficiente experiencia para construir una escuela.")
                else:
                    print("Construyendo una escuela...")
            elif nombre_edificio == "3": # HOSPITAL
                # Comprueba si el jugador tiene la experiencia necesaria para construir.
                if ciudad.experiencia < 200:
                    print("No tienes suficiente experiencia para construir un hospital.")
                else:
                    print("Construyendo un hospital...")
            else:
                print("Edificio no reconocido.")
        
        # --- LÓGICA DE FACTURACIÓN ---
        # Verifica si la acción elegida fue 'facturar'.
        if accion_limpia == "facturar":
            opcion_factura = input("¿Qué quieres facturar?\n1. Impuestos\n2. Servicios\n3. Vender\n4. Préstamos\n")
            if opcion_factura == "1": #IMPUESTOS
                print("¡Has elegido cobrar impuestos!")
                if ciudad.experiencia < 100:
                    porcentajeimpuestos = int(input("Elije el porcentaje de impuestos a cobrar. Al ser [NIVEL 1], puedes cobrar hasta un 10%: "))
                    if porcentajeimpuestos > 10:
                        print("No puedes cobrar más del 10% en este nivel.")
                    else:
                        # Se calcula el dinero a obtener basado en un porcentaje.
                        dineroapagar = ciudad.dinero * (porcentajeimpuestos / 100)
                        print(f"Los ciudadanos deben pagar {dineroapagar} monedas en impuestos.")
                        confirmarpago = input("¿Quieres continuar con la acción?\nEscribe [CONFIRMAR] si es así.\nEscribe [CANCELAR] para cancelar.")
                        # Si el jugador confirma, se actualiza el estado de la ciudad.
                        if confirmarpago.upper() == "CONFIRMAR":
                            print("Cobrando impuestos...")
                            ciudad.dinero = ciudad.dinero + dineroapagar
                            ciudad.experiencia = ciudad.experiencia + 10
                            ciudad.felicidad = ciudad.felicidad - 5
                            ciudad.mostrar_estado()
            elif opcion_factura == "2": #SERVICIOS
                print("Facturación de servicios no disponible.")
            elif opcion_factura == "3": #VENDER
                print("¡Has elegido vender bienes!")
            elif opcion_factura == "4": #PRÉSTAMOS
                print("¡Has elegido solicitar un préstamo!")
            else:
                print("Opción no válida.")

    # --- COMPROBACIONES DE ESTADO AL FINAL DEL TURNO ---
    # Comprueba si el jugador ha alcanzado la experiencia para subir de nivel.
    if ciudad.experiencia == 100:
        print("¡Felicidades! Has alcanzado el nivel 2. Como recompensa, ya puedes construir una escuela.\n¡WOW! Has conseguido 1000 monedas!")
        ciudad.dinero = ciudad.dinero + 1000
        ciudad.mostrar_estado()
    # Comprueba si el jugador ha alcanzado la experiencia para el siguiente nivel.
    if ciudad.experiencia == 200:
        print("¡Felicidades! Has alcanzado el nivel 3. Como recompensa, ya puedes construir un hospital.\n¡WOW! Has conseguido 2000 monedas!")
        ciudad.dinero = ciudad.dinero + 2000
        ciudad.mostrar_estado()
    # Condición de derrota: si la felicidad es muy baja, el juego termina.
    if ciudad.felicidad <= 10:
        print("¡LA FELICIDAD DE LA CIUDAD HA CAÍDO POR DEBAJO DEL 10%!<\n¡HA EMPEZADO UNA REVOLUCIÓN!\n")
        pygame.init()
        pygame.mixer.music.load("efectodestruccion.mp3")
        pygame.mixer.music.play() 
        time.sleep(7)
        print("¡LA CIUDAD HA SIDO DESTRUIDA!\n¡DERROTA! FIN DE LA PARTIDA")
        # Cierra el programa.
        sys.exit()

# --- PUNTO DE ENTRADA DEL SCRIPT ---
# Asegura que la función main() se ejecute solo cuando el script es el archivo principal.
if __name__ == "__main__":
    main()
