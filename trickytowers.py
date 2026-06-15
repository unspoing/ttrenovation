"""start the game"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from game import menu

if __name__ == "__main__":
    sys.exit(menu())
