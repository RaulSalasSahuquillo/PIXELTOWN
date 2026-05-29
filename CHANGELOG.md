# Changelog

All notable changes to the PIXELTOWN project will be documented in this file.

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
