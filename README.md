# PIXELTOWN 🏙️

Welcome to **PIXELTOWN**! This is a 2D city-building simulation game built with Python and Pygame. As the newly appointed leader, your job is to build the best city possible, managing resources, constructing buildings, and keeping your citizens happy. Beware—if their happiness drops too low, a coup d'état might destroy everything you've built!

## What is PIXELTOWN?

At its core, PIXELTOWN is a resource management and town-building game. You start with a small amount of money and a handful of citizens. From there, you must:
- **Build your town**: Construct houses, supermarkets, streetlights, and decorations.
- **Manage the economy**: Earn money from your inhabitants and spend it wisely in the shop.
- **Keep people happy**: Buy supplies (like soap and face masks) to boost happiness and gain experience. If happiness falls below 10%, your citizens will rebel!

## Features

- **User Accounts & Login**: Register new user accounts and log in securely right inside the terminal screen. Passwords are safe and encrypted locally using SHA-256 hashing.
- **Save & Load Progress**: Save your game state (net-worth, population, happiness, level, debt, experience, and custom buildings) dynamically. Easily reload your progress upon logging in.
- **Interactive UI**: Fully built with Pygame.
- **Resource Management**: Track your Money, Population, Happiness, Experience, Debt, and Town Level.
- **Building System**: Place different structures like houses, stores, streetlamps, and decorations dynamically on your map.
- **Store & Economy**: Buy items to boost stats or decorations to personalize your city.
- **Video Intro**: Plays a dynamic introduction video at startup using `pyvidplayer2`.
- **Guest Mode**: Play instantly without creating an account (saving progress is disabled).

## Prerequisites

Before you dive in, make sure you have the following installed:
- **Python 3.x**
- **Pygame / Pygame-CE**: Core engine for graphics and event handling.
- **Pyvidplayer2**: Used for rendering the video introduction.

You can install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

## Project Structure

The project is structured cleanly to keep the logic and assets organized:

- `src/`: Contains the core Python scripts (`main.py`, `game.py`, `terminal.py`, `localization.py`, etc.) and the `locals/` subdirectory containing `es.json` and `en.json` translation files.
- `assets/`: Contains all assets used by the game:
  - `imagenes/`: Visual assets, player sprites, and background images.
  - `PIXELTOWN_OST/`: Game soundtracks and sound effects.
  - `visual/`: Video elements such as `intro.mp4`.
- `saves/`: Contains local user credentials database (`accounts.json`) and player progress files (`<username>_save.json`). (This directory is ignored by Git).

## How to Play

1. **Clone or download** this repository.
2. Navigate to the project directory.
3. Run the main launcher:
   ```bash
   python src/main.py
   ```
4. Choose your language, then **register a new account** or **log in** with your username and password (or select **Play as Guest**).
5. If it's your first time, follow the onboarding prompts to enter your name and choose your city's name. Otherwise, it will load your previous progress automatically!
6. Click the **Save Progress** button inside the game map or exit normally to save your progress. Have fun and try not to get overthrown!

## Contributing

Contributions, issues, and feature requests are welcome! If you'd like to add new building types, tweak the economy, or just fix some bugs, check out the `CONTRIBUTING.md` file for more details. 

## License

This project is licensed under the **GNU General Public License v3 (GPL-3.0)**. See the `LICENSE` file for more information.

---

*Copyright (C) 2026 Raúl Salas Sahuquillo, ENEI PROJECT*