import sys
from img_processor import egg_count

if __name__ == "__main__":
    filenames = sys.argv[1:]
    
    for filename in filenames:
        egg_count(filename)
