# Changelog

All notable changes to the PIXELTOWN project will be documented in this file.

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
