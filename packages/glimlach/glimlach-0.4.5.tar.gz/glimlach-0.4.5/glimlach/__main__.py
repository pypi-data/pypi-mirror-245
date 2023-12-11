# __main__.py
import sys
from glimlach.cli import glimlach_main

def main():
    if len(sys.argv) != 2:
        print("Usage: glimlach <path_to_config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    glimlach_main(config_file)

if __name__ == "__main__":
    main()

