# Contributing to PIXELTOWN

Welcome! **PIXELTOWN** is a minimalist city-builder written in Python and Pygame. Contributions must align with these core principles to maintain the project's integrity.

## Core Principles

### Design Philosophy
- **Do one thing and do it well**: Every module or function in this project must focus on a single, well-defined task. Avoid "feature creep" or combining unrelated logic. For example, if a function calculates taxes, it should not also handle drawing menus on the screen.

### Laws of Minimalism
I adhere to a strict philosophy that emphasizes:
- **Simplicity**: Code must be direct, readable, and free of unnecessary abstractions. Avoid over-engineering: prefer straightforward solutions over complex design patterns or heavy frameworks.
- **Minimalism**: Eliminate code that doesn't have any purpose. **Zero external unverified dependencies** unless strictly necessary. Prioritize self-contained code, if you're able too.
- **Correctness**: Code must be robust and bug-free (especially memory leaks or FPS drops). Test rigorously and avoid "hacks" or temporary fixes.
- **Transparency**: Everything must be auditable. Zero hidden behaviors, "magic numbers" (hardcoding), or opaque logic.
- **No Bloat**: Reject unnecessary complexity. If a game mechanic feels overloaded, refactor it.

Contributions that violate these laws (e.g., adding heavy dependencies, increasing complexity without justification, or ignoring 60 FPS performance) will be rejected.

---

## Coding Guidelines

### Size Limits
- **Maximum lines per code block**: Each function, method, or independent logical unit must be **100 lines or fewer**. This forces focus and readability. Break down large logic into smaller, composable functions.
- **Exceptions**: Comments, blank lines, and pure configuration dictionaries do not count toward the line limit.
- **Justification**: Giant functions in Game Loops are impossible to debug, test, and maintain. This rule promotes absolute minimalism.

### Module Imports
- **Maximum imports per file**: Each file (e.g., a `.py` file) must include **5 external module imports or fewer**.
- Avoid importing entire libraries if unnecessary (prefer `from pygame.locals import *` over importing everything if you only use constants, or vice versa depending on context to maintain cleanliness).
- **Justification**: Excessive dependencies slow down game startup, increase RAM consumption, and clutter the namespace.

### General Coding Standards
- **Language**: Python 3.10+. Opened for extra languages you think that can fit.
- **Error Handling**: Use simple and explicit checks (`try/except`). Avoid silencing errors (`pass` in except blocks). Fatal asset loading errors must be clearly reported to the console using `sys.stderr` before closing the game.
- **Resource Management**: Memory and performance are vital. **NEVER** load resources (`pygame.image.load` or `pygame.mixer.Sound`) inside the main loop (`while True`). All assets must be loaded into memory once during initialization.
- **Testing**: Rigorous manual testing is recommended. Avoid heavy testing frameworks unless you are testing pure math or economics (separated from Pygame).
- **Documentation**: Use inline comments only for non-obvious logic. No external documentation unless the mechanic is genuinely complex.
- **Licensing**: All contributions become part of PIXELTOWN under its original terms.

---

## Current Modules

These are the existing tools and files. Read their source code before writing new ones to understand the expected style:

| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `main.py`          | Main loop at 60 FPS, state machine (scenes), and global variables           |
| `ciudad/ciudad.py` | (In development) Save structure and general city logic                      |
| `dinero.py`        | Economic management (earnings, expenses, population vs. taxes)              |
| `personaje.py`     | Player/inhabitant entities and variables                                    |
| `bloquegrafico.py` | Rendering logic for tiles, houses, and buildings on the map                 |
| `texto.py`         | Utility to simplify rendering Pygame fonts on screen                        |

---

## How to Contribute

1. **Fork and Clone**: Fork the repository, clone it locally, and create a descriptive branch for your changes.
2. **Understand the Base Code**: Review existing modules (e.g., `texto.py` for pure utilities, `main.py` to see how events and states are managed) for examples of compatible code.
3. **Make Your Changes**:
   - Ensure your code respects the size and import limits.
   - Run `python main.py` and ensure the game maintains a stable 60 FPS.
   - Verify there are no critical warnings in the terminal (Linting).
4. **Update README.md**: If you added a new file or dependency, include it in the corresponding section.
5. **Submit a Pull Request**:
   - Describe the change: What problem does it solve? How does it align with the project's minimalism principles?
   - Reference any open Issues if applicable.
6. **Review Process**: Compliance with principles, size limits, and quality will be verified. Be prepared to refactor if necessary.
7. **Language**: Contributions can be made in English and Spanish. No other languages are allowed.

---

## Acceptable Code Examples

**Simple Utility — `texto.py`** (clear and contained text rendering):
```python
import pygame

def draw_text(surface, text, font, color, x, y):
    """Renders text and positions it directly on the screen."""
    if not text or not font:
        return
    text_img = font.render(text, True, color)
    surface.blit(text_img, (x, y))