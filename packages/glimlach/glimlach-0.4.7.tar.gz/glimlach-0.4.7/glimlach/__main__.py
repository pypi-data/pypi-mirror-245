# run_docker_images/__main__.py

from glimlach.cli import run_docker_images_main
import argparse
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: glimlach <path_to_config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    run_docker_images_main(config_file)

if __name__ == "__main__":
    main()