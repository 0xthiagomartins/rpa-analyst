import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
src_dir = os.path.join(parent_dir, "src")
sys.path.insert(0, src_dir)

from src.app import main

if __name__ == "__main__":
    main()
