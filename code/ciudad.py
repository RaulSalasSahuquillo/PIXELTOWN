class Ciudad:
    def __init__(self, nombre):
        self.nombre = nombre
        self.dinero = 10000 # Dinero inicial
        self.poblacion = 10 # Población inicial
        self.edificios = 0 # Lista de edificios
        self.felicidad = 50 # Felicidad inicial
        self.experiencia = 0 # Experiencia inicial

    def mostrar_estado(self):
        print("\n📊 Estado actual de la ciudad:")
        print(f"Nombre: {self.nombre}")
        print(f"Dinero: {self.dinero} 💰")
        print(f"Población: {self.poblacion} 👥")
        print(f"Experiencia: {self.experiencia} 🧠")
        if self.felicidad > 50:
            print(f"Felicidad: {self.felicidad}% 🙂\n")
        elif self.felicidad < 50:
            print(f"Felicidad: {self.felicidad}% 🙁\n")
        else:
            print(f"Felicidad: {self.felicidad}% 😐\n")