#!/usr/bin/env python3
"""
PIXELTOWN - Launcher script.
Invokes main.py with the proper virtualenv interpreter if available.
"""
import os
import sys
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(base_dir, "PIXELTOWN_env", "bin", "python3")
    py_exec = venv_python if os.path.exists(venv_python) else sys.executable
    main_py = os.path.join(base_dir, "main.py")
    return subprocess.call([py_exec, main_py] + sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())
