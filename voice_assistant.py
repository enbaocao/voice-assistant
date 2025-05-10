#!/usr/bin/env python3
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main CLI
from src.cli.main import main

if __name__ == "__main__":
    main()