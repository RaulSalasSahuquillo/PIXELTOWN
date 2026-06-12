# Changelog

All notable changes to the PIXELTOWN project will be documented in this file.

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
