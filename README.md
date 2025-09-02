# PIXELTOWN

Un **city-builder** sencillo hecho con **Python + Pygame** (y una intro en vídeo con MoviePy). Este repositorio contiene el archivo principal del juego y la lógica de escenas/menús, además de las dependencias de imágenes, audio y módulos auxiliares. El juego se encuentra en fase Alpha Test for Developers y se irá actualizando regularmente.

---

## ✨ Características

* Intro en vídeo (`intro.mp4`) sincronizada a FPS con **MoviePy**.
* Menú principal con botón **JUGAR**.
* Flujo de onboarding en 2 preguntas: nombre del jugador y de la ciudad.
* HUD con **dinero, población, felicidad, edificios y experiencia**.
* Sistema de escenas: **mapa**, **acciones**, **tienda**, **información**, **facturar/impuestos**, **construcción** y **colocación de edificios**.
* Compra de productos que modifican estadísticas del jugador.
* Colocación de **casa**, **supermercado** y **Tarraco Import Export** con coste y recompensa de experiencia.
* Música y efectos con `pygame.mixer`.
* Mecanismo de **“game over”** si baja demasiado la felicidad.

---

## 🧩 Estructura de escenas (state machine)

```
intro → menu → (jugando → preguntando → preguntando2 → cargamapa → mapainicial)
mapainicial ↔ acciones ↔ {tienda, info, facturar}
info → infodos
facturar → {impuestos, vender_edificio, prestamo}   # (vistas WIP)
tienda → {construccion, productos, adorno, productos2}
construccion → colocando_edificio → mapainicial
```

---

## 📦 Requisitos

* **Python 3.10+**
* **Pygame 2.x**
* **moviepy** (para reproducir la intro)
* **numpy**, **imageio-ffmpeg** (dependencias de moviepy)
* Sistema operativo: Windows / macOS / Linux
* Tener instalado **pygame**, **sys**, **time** y **moviepy**
* **RECOMENDACIÓN:** Lo más fácil podría ser ejecutarlo a través de Visual Studio Code, ya que ha estado desarrollada desde allí y tiene las versiones exactas que requiere el juego

### Instalación rápida

```bash
# 1) Crear y activar entorno virtual (opcional, recomendado)
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

# 2) Instalar dependencias
pip install -U pip
pip install pygame moviepy numpy imageio imageio-ffmpeg
```

---

## ▶️ Ejecutar

Coloca todos los **assets** (imágenes, audio, vídeo) en el mismo directorio que el script principal o ajusta las rutas.

```bash
python main.py
```

Resolución por defecto: **1200 × 600**. FPS del loop: **60**.

---

## 🎮 Controles

* **Ratón**: clic en botones y para colocar edificios (izq. colocar, der. cancelar).
* **Teclado**: escribir respuestas en las pantallas de preguntas, **Enter** para enviar, **Backspace** para borrar.

---

## 📁 Árbol del proyecto (sugerido)

```
📂 PIXELTOWN
 ├── 📂 ciudad
 │    └── ciudad.py
 │
 ├── .gitignore
 ├── Aldea_soundtrack.mp3
 ├── BIENVENIDO.png
 ├── Casa.png
 ├── PIXELTOWN.png
 ├── PIXELTOWN_portada.png
 ├── adorno.png
 ├── anewbegining.mp3
 ├── bloquegrafico.py
 ├── construccion.png
 ├── dinero.py
 ├── efectoconstrucion.mp3
 ├── efectodestruccion.mp3
 ├── ganar_dinero.png
 ├── impuestos.png
 ├── info.png
 ├── intro.mp4
 ├── lovyc.png
 ├── lovyc_champu.png
 ├── lovyc_mascarilla.png
 ├── lovyc_monstruito.png
 ├── lovyc_toallitas.png
 ├── main.py
 ├── monstruito_pixel_kawaii_128.png
 ├── personaje.py
 ├── prestamo.png
 ├── productos.png
 ├── rio.png
 ├── supermercado.png
 ├── tarraco.png
 ├── texto.py
 ├── tienda.png
 └── venderedificio.png
```

> **Sugerencia:** evita tildes/espacios en los nombres de archivo (por ejemplo, usa `lovyc_champu.png` en vez de `lovyc_champú.png`) y actualiza las rutas en el código si cambias la organización (por ejemplo, `assets/img/Casa.png`).

---

## 🔊/🎞️ Assets y licencias

* Vídeo: `intro.mp4`
* Música: `anewbegining.mp3`, `Aldea_soundtrack.mp3`, `efectodestruccion.mp3`
* Imágenes: todas en formato .png

---

## ⚙️ Variables principales del juego

En `main.py` (o archivo principal):

```python
dinero = 10000
poblacion = 10
felicidad = 50
experiencia = 0
dineroporhabitante = 1000
stock = 0        # Todavía en desarrollo
stock_maximo = 1000    # Todavía en desarrollo
edificios = []   # {"tipo": str, "pos": (x, y)}
```

---

## 🧪 Ejecución de la intro

La intro usa MoviePy para reproducir `intro.mp4` fotograma a fotograma sincronizado al `Clock()` de Pygame. Si no se encuentra el vídeo o hay error, el juego **salta la intro** y continúa al menú.

---

## 🛠️ Empaquetado (opcional)

Con **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" main.py
```

* En Windows, separa con `;`. En macOS/Linux usa `:` en `--add-data`.
* Asegúrate de copiar `imageio_ffmpeg` si MoviePy lo requiere.

---

## 🧯 Solución de problemas (FAQ)

* **“No se pudo cargar la imagen …”**
  Verifica la **ruta** y el **formato**. Evita tildes/espacios y respeta mayúsculas/minúsculas.
* **“No se pudo cargar el archivo de música …”**
  Comprueba que el formato sea compatible con `pygame.mixer` y que el dispositivo de audio esté disponible.
* **La intro no se ve / se oye**
  Asegura `imageio-ffmpeg` instalado: `pip install imageio-ffmpeg`.
  En macOS puede necesitar permisos de pantalla/sonido.
* **ImportError con MoviePy**
  Usa `from moviepy.editor import VideoFileClip` y reinstala `moviepy`: `pip install -U moviepy`.

  Si no funciona `moviepy.editor`, tal vez tengas que cambiarlo al importarlo y poner solamente `moviepy`.

---

## 🗺️ Roadmap

* Mapa por tiles y colisiones básicas.
* Balanceo de economía y felicidad por edificio/acción.
* Guardado/carga de partidas (JSON).
* UI mejorada (estilos, iconos, tooltips).
* Sonido/música configurables y tabla de volúmenes.
* Internacionalización (ES/EN/ZH). El juego actualmente solo está disponible en Español.
* Tests unitarios de lógica (sin Pygame).

---

## 🤝 Contribuir

1. Haz un fork y crea una rama: `git checkout -b feature/mi-mejora`.
2. Sigue la guía de estilo (PEP 8) y añade comentarios claros.
3. Prueba en local y abre un **Pull Request** con una descripción concisa.

---

## 🙌 Créditos

* Desarrollo del juego: **PIXELTOWN** (ENEI PROJECT/Raúl Salas Sahuquillo).
* Librerías: [Pygame](https://www.pygame.org/), [MoviePy](https://zulko.github.io/moviepy/).
* Arte/música: la música ha estado creada por el desarrollador a través de Suno.ai y este tiene todos los derechos de autor.
* No te olvides de seguir nuestras redes sociales!

---

## 📝 Notas para el repositorio

* Para facilitar la instalación:

  ```txt
  pygame>=2.5
  moviepy>=1.0
  numpy>=1.24
  imageio>=2.34
  imageio-ffmpeg>=0.4
  ```

* Evita **caracteres acentuados** en nombres de archivos. Sin embargo, están permitidos en las cajas de texto.

---

¡Disfruta construyendo tu ciudad pixelada! 🏙️🧱💰
