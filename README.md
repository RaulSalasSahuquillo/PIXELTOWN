# PIXELTOWN 🏙️

Welcome to **PIXELTOWN**! This is a 2D city-building simulation game built with Python and Pygame. As the newly appointed leader, your job is to build the best city possible, managing resources, constructing buildings, and keeping your citizens happy. Beware—if their happiness drops too low, a coup d'état might destroy everything you've built!

## What is PIXELTOWN?

At its core, PIXELTOWN is a resource management and town-building game. You start with a small amount of money and a handful of citizens. From there, you must:
- **Build your town**: Construct houses, supermarkets, streetlights, and decorations.
- **Manage the economy**: Earn money from your inhabitants and spend it wisely in the shop.
- **Keep people happy**: Buy supplies (like soap and face masks) to boost happiness and gain experience. If happiness falls below 10%, your citizens will rebel!

## Features

- **Interactive UI**: Fully built with Pygame.
- **Resource Management**: Track your Money, Population, Happiness, and Experience.
- **Building System**: Place different structures like houses and stores dynamically on your map.
- **Store & Economy**: Buy items to boost stats or decorations to personalize your city.
- **Video Intro**: Uses `moviepy` to render a video cutscene at launch.

## Prerequisites

Before you dive in, make sure you have the following installed:
- **Python 3.x**
- **Pygame**: Core engine for graphics and event handling.
- **MoviePy**: Used for rendering the video introduction.

You can install the required dependencies using pip:
```bash
pip install pygame moviepy
```

## Project Structure

The project is structured cleanly to keep the logic and assets organized:

- `code/`: Contains the core logic scripts (`main.py`, `characters.py`, `text.py`, etc.).
- `imagenes/`: Visual assets, player sprites, and background images.
- `audios/`: Game soundtracks and cool sound effects.
- `visual/`: Video elements such as `intro.mp4`.

## How to Play

1. **Clone or download** this repository.
2. Navigate to the project directory and open the `code/` folder.
3. Run the main file:
   ```bash
   cd code
   python main.py
   ```
4. Follow the on-screen prompts to enter your name and your city's name to begin your mayoral journey. Have fun and try not to get overthrown!

## Contributing

Contributions, issues, and feature requests are welcome! If you'd like to add new building types, tweak the economy, or just fix some bugs, check out the `CONTRIBUTING.md` file for more details. 

## License

This project is licensed under the **GNU General Public License v3 (GPL-3.0)**. See the `LICENSE` file for more information.

---

*Copyright (C) 2026 Raúl Salas Sahuquillo, ENEI PROJECT*