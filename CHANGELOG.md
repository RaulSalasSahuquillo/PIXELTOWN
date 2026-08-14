# Changelog

All notable changes to the PIXELTOWN project will be documented in this file.

## [2.2.7] - 2026-08-14

### Changed / Refactored
- **English Codebase Translation**:
  - Translated all variable names, function names, and parameters across `src/game.py`, `src/text.py`, `src/characters.py`, `src/snake.py`, `src/solarsystem.py`, `src/tetris.py`, `src/terminal.py`, and `src/main.py` from Spanish to English.
  - Maintained JSON save file compatibility (`"nombre_usuario"`, `"nombre_ciudad"`, `"dinero"`, etc.) for existing game saves.
- **English Assets & Image Filenames Translation**:
  - Renamed asset directory from `assets/imagenes/` to `assets/images/`.
  - Renamed all Spanish image filenames to English (`house.png`, `supermarket.png`, `streetlamp.png`, `ornament_mytownmyrules.png`, `bush.png`, `pixeltown_cover.png`, `welcome.png`, `river.png`, `shop.png`, `earn_money.png`, `minigames.png`, `construction.png`, `products.png`, `decoration.png`, `lovyc_mask.png`, `lovyc_shampoo.png`, `lovyc_wipes.png`, `taxes.png`, `sell_building.png`, `loan.png`, etc.).
  - Updated all image loading references (`pygame.image.load`) across the codebase to match the new English asset path and image filenames.

## [2.2.6] - 2026-08-12

### Added
- **Exit Button on Info2**:
  - Added a red button with an "X" to return to the `mapainicial` page
- **Alert**:
  - Added an alert text that matches the things printed in the terminal, but is displayed on screen
  - Used for `cannot_build_on_river`
- **Sound Toggle**
  - Added a mute/unmute sound button
  - When pressed, it will mute/unmute the background music, and change the icon accordingly
  - Shown in `menu` page and `mapainicial` page
- **`mouseDown` Variable**
  - Added a `mouseDown` variable that correlates to if the mouse was down or not in the previous frame
  - Used in sound toggle and exit/quit buttons
- **Death Screen**
  - Added a death screen after the town runs out of happiness
  - Displays `"GAME OVER"`, reason of death, and a quit button to exit the application
- **Width and Height variable**
  - Added a width and height variable to easily set the size and coordinates of things
  - Used in all full screen applicants, and the quit screen

### Fixed
- **River Hitbox**
  - Adjusted river hitbox for no placing on the river to cover just outside the bounds of the river
- **Button Text Color**
  - Changed all text color within buttons on the initial screen from an unreadable white to a contrasting black

## [2.2.5] - 2026-08-09

### Added
- **River Building Restriction**:
  - Buildings can no longer be placed on top of the river in the placement scene (`escena_colocacion`).
  - Added collision detection between the building ghost and the river area (`pygame.Rect(450, 200, 300, 300)`).
  - Added localized feedback message (`cannot_build_on_river`) when the player attempts to build on the river.
- **Localization**:
  - Added new translation keys to `es.json` and `en.json`: `cannot_build_on_river`, `placement_cancelled`, `available_buildings`, `sells_for`, `no_buildings_to_sell`, `error_saving_account`.
  - Replaced all remaining hardcoded Spanish strings in `src/game.py` and `src/terminal.py` with localized `_()` calls.
  - Building names in `EDIFICIOS_CONFIG` now use translation keys (`nombre_key`) instead of hardcoded Spanish names, making them fully translatable.

### Fixed
- **Minigame Freeze Bug**:
  - Fixed an issue introduced in v2.2.0 where the Snake, Tetris, and Solar System minigames would freeze on launch due to the window scaling monkey-patches interfering with the minigames' own game loops.
  - Added a `_minigame_active` bypass flag that disables coordinate transformations while a minigame is running, and properly restores the virtual surface system on return.
- **English Typo**:
  - Fixed `"recieved"` → `"received"` in the `borrow_collected` translation key.

## [2.2.0] - 2026-07-09

### Added
- **Tkinter GUI Login Launcher**:
  - Replaced the legacy terminal-based login/registration menu with a graphical user interface (GUI) using Tkinter.
  - Implemented language selection buttons (Spanish and English) with styled flag indicators.
  - Added user authentication card forms featuring placeholders, hidden characters for passwords, input validation, error alerts/status labels, guest play mode, and window icon.
- **Window Resizing and Scale Support**:
  - Added custom wrapper overrides in `src/game.py` for Pygame display, mouse, and event subsystems.
  - Implemented handling for the `pygame.VIDEORESIZE` event to allow players to resize the game window dynamically.
  - Scaled coordinates and relative motion offsets for mouse input events dynamically, keeping them mapping to the internal 1200x600 virtual screen size.

### Changed
- **Dependencies**:
  - Documented requirement of system Tkinter library (`python3-tk` on Linux/Ubuntu platforms).
  - Cleaned up `requirements.txt` by removing obsolete packages (`moviepy`, `tqdm`, `proglog`, `imageio-ffmpeg`, `ImageIO`, `decorator`, `python-dotenv`).
- **Project Structure**:
  - Updated all documentation files (`README.md`, `CONTRIBUTING.md`, and Web IDE pages) to correctly reference the complete Python source files inside `src/`.

## [2.1.0] - 2026-07-05

### Added
- **Building Selling System**:
  - Implemented the `vender_edificio` scene/screen that displays built buildings and allows the player to click on them to sell them.
  - Automatically pays off outstanding debt first using the selling price profit.
  - Returns 50% of the building's cost (in money) and 50% of the experience reward back to the player.
  - Added a localized "SELL BUILDING" button in the `facturar` screen transitioning to this scene.
- **Global Building Configuration**:
  - Centralized the building definitions from `escena_colocacion` into a module-level `EDIFICIOS_CONFIG` dictionary.
  - Added helper functions (`obtener_precio_venta`, `obtener_experiencia_venta`, and `obtener_nombre_edificio`) to simplify retrieve operations.
- **Localization**:
  - Added translation keys (`sell_building`, `click_building_to_sell`, `loan_repaid`, `loan_partially_repaid`, `building_sold`, `click_to_sell`) in Spanish (`es.json`) and English (`en.json`).

## [2.0.0] - 2026-06-24

### Added
- **User Account System**:
  - Implemented interactive console registration and login prompts inside `terminal.py`.
  - Secured player credentials by hashing passwords with SHA-256, writing to `saves/accounts.json`.
  - Hidden password entries during console inputs using python's `getpass` module.
- **Game Progress Saving**:
  - Added game state serialization storing player stats (money, population, happiness, level, debt, and experience) and town buildings dynamically to JSON files (`saves/<username>_save.json`).
  - Added a new localized **Save Progress** button on the `mapainicial` Pygame screen.
  - Provided floating on-screen confirmation banners ("Progress saved!") for 3 seconds after saving.
  - Implemented automatic progress saving on normal game exit and when finishing the initial onboarding questions.
- **Guest Mode**:
  - Added a guest access choice that launches the game without account requirements, displaying a disabled "Guest Mode" button.
- **Localization**:
  - Added new Spanish and English translation keys to support login menus, status feedback, and guest warning tags.

### Fixed
- **Duplicate JSON Closing Braces**:
  - Fixed syntax errors in `en.json` caused by extra trailing brackets.

## [1.7.0] - 2026-06-12

### Added
- **Tetris Minigame**:
  - Integrated `tetris.py` as a playable minigame inside PIXELTOWN.
  - Created `run_tetris(pantalla)` using an exception-based pattern (`_TetrisExit`) to cleanly break out of nested game loops.
  - After Game Over, the player is returned to the minigames menu instead of restarting.
  - Pressing ESC during gameplay also returns to the minigames menu.
- **Solar System Simulator Minigame**:
  - Merged `solarsystem.py` (planet data) and `simulator.py` (simulation logic) into a single `solarsystem.py` module.
  - Created `run_solarsystem(pantalla)` following the same integration pattern as Snake and Tetris.
  - Added an on-screen EXIT button (top-right corner) to return to the minigames menu.
  - Fixed all image paths to use `assets/imagenes/` via `os.path.join()`.
  - Removed fullscreen mode and `sys.exit()` calls; the simulator now reuses the PIXELTOWN display.
- **Localization**:
  - Added `"tetrisgame"` key to `es.json` ("Tetris") and `en.json` ("Tetris").
  - Added `"solarsystem"` key to `es.json` ("Sistema Solar") and `en.json` ("Solar System").

### Fixed
- **Minigames Menu Layout**:
  - Snake and Tetris buttons were overlapping at the same screen position — now laid out side by side.
  - Tetris button was incorrectly labelled as `"snakegame"` — now uses `"tetrisgame"`.
  - Tetris button click check used `boton_snake` instead of `boton_tetris` — fixed.
- **Game Loop**:
  - The `"tetrisgame"` state was calling `minijuegos(pantalla)` instead of `tetrisgame(pantalla)` — fixed.

### Removed
- **`simulator.py`**: Deleted; all code merged into `solarsystem.py`.

## [1.6.7] - 2026-06-08

### Added
- **Stats Button**
  - Added a button to view the stats.

### Fixed
- **Pygame Event AttributeError**
  - Fixed a crash where non-mouse events (like keyboard key presses or window quit events) caused the game to crash on the initial map scene because they lacked the `.pos` attribute.

### Changed
- **Stats Button Layout**
  - Repositioned the "View stats" button to the top-right corner of the screen and reduced its size to look cleaner.

## [1.6.6] - 2026-05-26

### Added
- **Levels**
  - Now there are levels depending on the experience you have.

### Fixed
  - Position of stats have the same space.

### Changed
  - Logic on earning experience. 

## [1.6.5] - 2026-05-26

### Added
- **Logo**
  - PIXELTOWN now has its own logo, only for Windows users.

### Changed
- **Intro Video**
  - To accelerate the process, I changed the moviepy library to pyvidplayer2, since it is based in C, so it runs faster.

### Fixed
- **Debt Logic**
  - Fixed some bugs in loans.

## [1.6.0] - 2026-05-28

### Added
- **Debt logic**
  - Now you can't borrow more than 30% of your net-worth.
  - You can't type characters in the borrowing text box.

### Fixed
- **Stats**
  - Debt was overwritten on the 'experience' info.
  - The quantity of debt wasn't shown on the stats.
  - The problem about pygame not reading \n properly is now fixed.

## [1.5.0] - 2026-05-28

### Added
- **Dynamic Localization Engine**:
  - Created `src/localization.py` to handle loading language resources and dynamically translating text keys at runtime.
  - Added `src/locals/es.json` containing all Spanish translations for menus, stats, notifications, and info screens.
  - Added `src/locals/en.json` containing matching English translations.

### Changed
- **Consolidated Game Source**:
  - Unified the separate language-specific game files (`main_es.py` and `main_en.py`) into a single, dynamic codebase (`src/game.py`).
  - Merged text templates into `src/text.py` using resource-driven localization.
- **Codebase Reorganization**:
  - Relocated all active python source files to a clean `src/` directory.
  - Restored `src/main.py` and `src/terminal.py` launcher connections to use the original module functions (`game.main`).

## [1.0.0] - 2026-05-27

### Added
- **Multi-language Support**: 
  - Added a language selector console screen at startup to choose between Spanish and English.
  - Added a fully localized English edition of the game (`main_en.py`) with all buttons, terminal messages, prompts, status screens, and logs translated.
  - Created `text_en.py` to store English translations for intro text, warnings, and informational panels.
- **Unified Assets Folder**:
  - Reorganized directory structure to place all game assets under the `assets/` root folder (comprising `imagenes/`, `PIXELTOWN_OST/`, and `visual/`).
- **Entry Launcher**:
  - Added `main.py` as a lightweight launcher entry point that displays the terminal selection.

### Fixed
- **Circular Imports**:
  - Resolved circular dependency issues between the terminal script and game loop logic by dynamically loading the selected language module locally.
