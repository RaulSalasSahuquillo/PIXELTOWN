# Changelog

All notable changes to the PIXELTOWN project will be documented in this file.

## [Beta v3.1.3] - 2026-09-25

### Added
- **Sequential Village Soundtrack Playback (OST Playlist)**:
  - Implemented continuous sequential playback of all OST soundtracks located in `assets/PIXELTOWN_OST/` (`Aldea_soundtrack.ogg`, `THIS_IS_PIXELTOWN.ogg`, `WeAreChampions.ogg`, `anewbegining.ogg`, `wHy so seRioUs¿.ogg`) once inside the village.
  - Songs now play in a seamless rotation: when one track finishes, the next track immediately starts automatically, looping back to the beginning upon reaching the end of the playlist.
  - Added automatic sound effect filtering to exclude non-music audio files (such as `efectoconstruccion.ogg`) from the background music playlist.
  - Preserved mute/unmute volume state across sequential track transitions.
  - Fixed audio transition when loading saved games directly into the village, ensuring the village playlist begins immediately instead of continuing the title menu music.

### Changed
- **Minigame Audio Pause State**:
  - Updated Tetris pause menu in `src/tetris.py` to use `pygame.mixer.music.pause()` and `pygame.mixer.music.unpause()`, preventing tracks from restarting from 0 or resetting playlist state.

## [Beta v3.1.2] - 2026-09-07

### Fixed
- **Pygame Rendering Performance & Asset Caching**:
  - Migrated uncached per-frame `pygame.image.load()` and `pygame.transform.scale()` calls across multiple menus (`game_scene`, `actions_scene`, `shop_scene`, `products_scene`, `products_two_scene`, `billing_scene`, `minigames_scene`) to use the unified `get_cached_image()` cache, eliminating hundreds of synchronous disk reads and surface allocations per second.
  - Eliminated the per-frame 14-building image loading and scaling loop in `sell_building_scene` by introducing a centralized `get_building_images()` cache.
  - Reused cached building icon surfaces in `initial_map_scene` and `placement_scene`, preventing redundant dictionary construction on every frame.
  - Implemented `get_cached_font()` to cache TrueType font instances by name and size, resolving per-frame font re-instantiations in `show_alert`, `info_two_scene`, and `gameover_scene`.
  - Cached the UI font in `src/solarsystem.py` (`_ui_font`) to avoid creating `pygame.font.Font` each frame in the Solar System simulator.
  - Removed duplicate `pygame.display.flip()` call in `gameover_scene` to prevent display tearing and double buffer swapping.

## [Beta v3.1.1] - 2026-09-06

### Changed
- Converted all audio files from `.mp3` to `.ogg` for pygbag support
- Updated the code to look for `.ogg` files instead

## [Beta v3.1] - 2026-09-02

### Added
- **Pygbag WebAssembly & Localhost Browser Export**:
  - Implemented full WebAssembly browser export using Pygbag (`pygbag.ini`, `web_template.tmpl`).
  - Added dynamic port detection with automatic fallback to port 8001 when port 8000 is occupied by other processes (e.g. FastAPI / Uvicorn).
  - Declared PEP 723 dependency metadata (`# /// script`) in `main.py` ensuring automated runtime packaging of `pygame-ce`.
  - Added bilingual web startup flow with dynamic query string detection (`?lang=en`, `?lang=es`), `localStorage` persistence, and browser locale fallback (`navigator.language`).
  - Integrated floating in-browser language switcher widget (`🌐 🇪🇸 ES | 🇬🇧 EN`) on the web canvas page for instant language switching without leaving the browser.
- **Language-First Tkinter Dual-Mode Launcher**:
  - Implemented interactive launcher GUI (`start_launcher.py` / `src/terminal.py`).
  - **Step 1**: Prompts user first for preferred language (`🇪🇸 Español` vs `🇬🇧 English`).
  - **Step 2**: Prompts for execution platform in the chosen language (`🖥️ Classic Pygame Window` vs `🌐 Web Localhost Format (pygbag)`).
  - Integrated background subprocess management to launch, monitor live terminal logs, auto-open the browser, and stop the local Pygbag server cleanly.

### Fixed
- **Cross-Platform Surface Scaling in WebAssembly**:
  - Resolved `ValueError: Source and destination surfaces need to be compatible formats` when scaling virtual display surfaces to the Emscripten SDL2 canvas in `custom_flip()` and `custom_update()` (`src/game.py`) via safe adaptive blit fallback.
- **Dynamic CDN Port Proxying in Pygbag**:
  - Patched Pygbag internal CDN host lookup to dynamically map to the active server proxy port (8001) instead of hardcoded port 8000, eliminating CORS download failures on wheel dependencies.
- **Web Video Driver Context Initialization**:
  - Resolved `pygame.error: The video driver did not add any displays` by synchronizing `start_toplevel()` with user media activation (`MM.UME`) and clear start button prompting.
- **Module Imports Compatibility in Minigames**:
  - Added safe attribute extraction fallback for `from pygame.locals import *` in `src/tetris.py` to prevent WASM modular import failure.
  - Fixed early display reference in `src/spaceship.py` (`BORDER`, `YELLOW_HIT`, `RED_HIT`) by deferring rect creation until display initialization.

## [Beta v3.0.1] - 2026-08-24


### Changed
- **Branding & Credits Update**:
  - Removed all references to `ENEI PROJECT` across the entire codebase, documentation (`README.md`, `LICENSE`), web portal (`docs/index.html`), GUI footers, and Python source file headers.
  - Added dedicated **Greetings** (Lead Developer: Raúl Salas Sahuquillo) and **Contributors** (Leanna Lee) sections to the in-game Information screen (`src/locals/en.json`, `src/locals/es.json`).
  - Removed Discord community links and interactive button from the Info screen.
- **Intro Scene Replacement**:
  - Replaced the startup video intro with a clean minimalist black-background splash screen displaying `"A game made by Raúl Salas"` with smooth fade-in/fade-out transitions and skip functionality before entering the title menu.

## [Beta v3.0] - 2026-08-21

### Added
- **Missions & Objectives System**:
  - Implemented interactive `missions_scene` accessible via the Actions menu (`actions_scene`), introducing structured gameplay progression.
  - Added mascot companion Toy (Pink Monster) with animated sliding entrance, typewriter text dialogue effect, and dynamic talking states (`toy.png`, `toyspeaking.png`).
  - Added 5 initial missions with milestone checks and rewards:
    1. *First Steps*: Build your first Simple House (+100 Money, +50 EXP).
    2. *Municipal Savings*: Reach 1,500 Money (+200 Money, +50 EXP).
    3. *Feed the City*: Build a Supermarket (+300 Money, +100 EXP).
    4. *Higher Level Mayor*: Reach City Level 2 (+500 Money, +150 EXP).
    5. *Growing Metropolis*: Build 3 total buildings (+400 Money, +100 EXP).
  - Added reward claiming mechanic and state persistence (`current_mission`, `completed_missions` saved in user profile JSON).
- **Spaceship Battle Minigame**:
  - Added `src/spaceship.py`, a retro 2D space duel minigame integrated seamlessly into the minigames menu (`minigames_scene`).
  - Implemented 1P (vs AI) mode with dodging, tracking, and shooting AI behaviors, and 2P (PvP) local multiplayer mode (`WASD + K` vs `Arrows + RCtrl`).
  - Added particle systems (thruster trails, projectile spark collisions, bullet clash explosions), health bars, and sound effects (`Gun+Silencer.mp3`, `Grenade+1.mp3`).
  - Connected victory rewards: winning against the AI grants +25 Money and +25 XP to the city.
- **20-Photogram Retro Pixel-Art Animated Title Screen**:
  - Added `src/pixeltown_titlescreen.py` featuring a 20-frame procedural pixel-art animation of Toy building Pixeltown with parallax clouds, rotating windmill, crane, and CRT scanline overlay.
  - Added 20 high-resolution photogram frames in `assets/images/` (`pixeltown-photogram-frame-01-4x.png` to `pixeltown-photogram-frame-20-4x.png`).
  - Set as the active animated background for the main menu screen (`menu_scene`).
- **Expanded Building Catalog (6 New Buildings)**:
  - Added Mail Office / Post Office (`mailoffice` - $400, +25 XP).
  - Added Restaurant (`restaurant` - $600, +40 XP).
  - Added Gym (`gym` - $700, +45 XP).
  - Added School (`school` - $1,000, +60 XP).
  - Added Police Station (`policestation` - $1,200, +75 XP).
  - Added Town Hall / Ayuntamiento (`townhall` - $2,000, +120 XP).
  - Redesigned `construction_scene` into a modern 3x3 responsive card layout with image previews, cost/EXP badges, and interactive build buttons.
- **Expanded Decoration Catalog (6 New Ornaments)**:
  - Added Fountain (`fountain` - $150, +15 XP).
  - Added Tree (`tree` - $30, +3 XP).
  - Added Statue (`statue` - $200, +20 XP).
  - Added Water Feature (`water_feature` - $120, +12 XP).
  - Added Trash Can (`trashcan` - $15, +1 XP).
  - Added Sewer (`sewer` - $25, +2 XP).
  - Redesigned `decoration_scene` into a 3x3 grid with per-decoration build limits (max 5 per type) and live count tracking.
- **Minigame Economy & City Progression Integration**:
  - Created `add_reward(money, exp)` system bridging arcade minigames with the main city economy.
  - **Snake Game (`src/snake.py`)**: Grants +5 Money and +5 XP per food consumed, with floating popup feedback (`+5 Money +5 XP!`) and real-time HUD reward stats.
  - **Tetris Game (`src/tetris.py`)**: Grants +10 Money and +10 XP per line cleared with in-game reward display (`+X$ +XXP`).
- **Tarraco Commercial Requirement**:
  - Added commercial prerequisite check to `products_scene` and `products_two_scene`: players must construct Tarraco Import Export before purchasing Lov'yc hygiene products, complete with on-screen warnings and alerts.
- **Branding, Startup & Policy Documentation**:
  - Added stylized ASCII title banner (`terminal_title()`) in `src/text.py` and GNU GPL v3 notice on startup in `src/main.py`.
  - Added `CODE_OF_CONDUCT.md` (Contributor Covenant v2.0) and `SECURITY.md` (vulnerability disclosure policy).
  - Updated high-resolution sound toggle button assets (`soundon.png`, `soundoff.png`).

### Changed
- **Localization Engine**:
  - Enhanced `src/localization.py` with `get_language()`, `current_lang` tracker, and automatic language fallback loading.
  - Added comprehensive Spanish (`es.json`) and English (`en.json`) translation strings for all new buildings, decorations, missions, dialogues, minigames, warnings, and updated info screens.
- **Dependencies**:
  - Updated `requirements.txt` to include runtime and packaging libraries (`pyinstaller`, `moviepy`, `opencv-python`, `pillow`, `sounddevice`, `pyvidplayer2`, etc.).

## [Beta v2.2.7] - 2026-08-14

### Changed / Refactored
- **English Codebase Translation**:
  - Translated all variable names, function names, and parameters across `src/game.py`, `src/text.py`, `src/characters.py`, `src/snake.py`, `src/solarsystem.py`, `src/tetris.py`, `src/terminal.py`, and `src/main.py` from Spanish to English.
  - Maintained JSON save file compatibility (`"nombre_usuario"`, `"nombre_ciudad"`, `"dinero"`, etc.) for existing game saves.
- **English Assets & Image Filenames Translation**:
  - Renamed asset directory from `assets/imagenes/` to `assets/images/`.
  - Renamed all Spanish image filenames to English (`house.png`, `supermarket.png`, `streetlamp.png`, `ornament_mytownmyrules.png`, `bush.png`, `pixeltown_cover.png`, `welcome.png`, `river.png`, `shop.png`, `earn_money.png`, `minigames.png`, `construction.png`, `products.png`, `decoration.png`, `lovyc_mask.png`, `lovyc_shampoo.png`, `lovyc_wipes.png`, `taxes.png`, `sell_building.png`, `loan.png`, etc.).
  - Updated all image loading references (`pygame.image.load`) across the codebase to match the new English asset path and image filenames.

## [Beta v2.2.6] - 2026-08-12

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

## [Beta v2.2.5] - 2026-08-09

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

## [Beta v2.2.0] - 2026-07-09

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

## [Beta v2.1.0] - 2026-07-05

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

## [Beta v2.0.0] - 2026-06-24

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

## [Beta v1.7.0] - 2026-06-12

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

## [Beta v1.6.7] - 2026-06-08

### Added
- **Stats Button**
  - Added a button to view the stats.

### Fixed
- **Pygame Event AttributeError**
  - Fixed a crash where non-mouse events (like keyboard key presses or window quit events) caused the game to crash on the initial map scene because they lacked the `.pos` attribute.

### Changed
- **Stats Button Layout**
  - Repositioned the "View stats" button to the top-right corner of the screen and reduced its size to look cleaner.

## [Beta v1.6.6] - 2026-05-26

### Added
- **Levels**
  - Now there are levels depending on the experience you have.

### Fixed
  - Position of stats have the same space.

### Changed
  - Logic on earning experience. 

## [Beta v1.6.5] - 2026-05-26

### Added
- **Logo**
  - PIXELTOWN now has its own logo, only for Windows users.

### Changed
- **Intro Video**
  - To accelerate the process, I changed the moviepy library to pyvidplayer2, since it is based in C, so it runs faster.

### Fixed
- **Debt Logic**
  - Fixed some bugs in loans.

## [Beta v1.6.0] - 2026-05-28

### Added
- **Debt logic**
  - Now you can't borrow more than 30% of your net-worth.
  - You can't type characters in the borrowing text box.

### Fixed
- **Stats**
  - Debt was overwritten on the 'experience' info.
  - The quantity of debt wasn't shown on the stats.
  - The problem about pygame not reading \n properly is now fixed.

## [Beta v1.5.0] - 2026-05-28

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

## [Beta v1.0.0] - 2026-05-27

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
