# IMPORTAR LIBRERIAS
from ciudad.ciudad import Ciudad
from texto import titulo
from mapa import mostrar_mapaascii
from mapa import mostrar_mapagrafico
from bloquegrafico import rio
from bloquegrafico import edificio1

# FUNCION MAIN
def main():
    titulo()
    print("¡Bienvenido a PixelTown!")
    tu_nombre = input("¿Cómo te llamas? ")
    nombre_ciudad = input("¿Cómo quieres llamar a tu ciudad? ")

    print("¡Empieza la gestión de tu ciudad!")

    while True:
        tipo_mapa = int(input("Elige el tipo de mapa:\n1. Mapa en ASCII\n2. Mapa gráfico\n3. Preview de los mapas\n"))
        if tipo_mapa == 1:
            print("\nHas elegido un mapa en ASCII.")
            break
        elif tipo_mapa == 2:
            print("\nHas elegido un mapa gráfico.")
            break
        elif tipo_mapa == 3:
            print("\nAquí puedes ver una vista previa de los mapas.\n MAPA EN ASCII:")
            mostrar_mapaascii()
            print("\n MAPA GRÁFICO:")
            mostrar_mapagrafico()
                    
    if tipo_mapa == 1:
        print(f"Bienvenido a la ciudad de {nombre_ciudad}, {tu_nombre}!\n")
        ciudad = Ciudad(nombre_ciudad)
        ciudad.mostrar_estado()
        print("Cargando datos iniciales del mapa...")
        rio()
        while True:
            accion = input("Escribe la acción que deseas realizar: \nConstruir\nVender\nAlimentar\n")
            accion_limpia = accion.strip().lower()
            if accion_limpia == "construir":
                print("Has elegido construir un edificio.")
                break
            elif accion_limpia == "vender":
                print("Has elegido vender un edificio.")
                break
            elif accion_limpia == "alimentar":
                print("Has elegido alimentar a la población.")
                break
            else:
                print("Acción no reconocida. Vuelve a intentarlo.\n")
        
        if accion_limpia == "construir":
            nombre_edificio = input("¿Qué edificio quieres construir?\n 1. Casa\n 2. Escuela\n 3. Hospital\n 4. Piso\n")
            if nombre_edificio == "1":
                print(f"Información sobre la casa:\nCosto: 1000\nEdificios totales: {ciudad.edificios + 1}\nDinero restante: {ciudad.dinero - 1000}\nFelicidad: {ciudad.felicidad + 5}%\nExperiencia: {ciudad.experiencia + 10}")
                confirmacion = input("¿Quieres continuar con la compra? Escribe [CONFIRMAR] si es así.\nEscribe [CANCELAR] para cancelar.\n")
                if confirmacion == "CONFIRMAR":
                    edificio1()
                    rio()
                    print("Edificio construido.")
                    ciudad.edificios = ciudad.edificios + 1
                    ciudad.dinero = ciudad.dinero - 1000
                    ciudad.felicidad = ciudad.felicidad + 5
                    ciudad.experiencia = ciudad.experiencia + 10
                    ciudad.mostrar_estado()
                if confirmacion == "CANCELAR":
                    print(f"Compra cancelada. ¡La felicidad de la población ha disminuido un 5%! Actualmente es: {ciudad.felicidad - 5}%")
            elif nombre_edificio == "2":
                print("Construyendo una escuela...")
            elif nombre_edificio == "3":
                print("Construyendo un hospital...")
            else:
                print("Edificio no reconocido.")

if __name__ == "__main__":
    main()
    
