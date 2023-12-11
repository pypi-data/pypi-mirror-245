# run_docker_images/__main__.py

from run_docker_images.cli import run_docker_images_main
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: run-docker-images <path_to_config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    run_docker_images_main(config_file)

if __name__ == "__main__":
    main()
