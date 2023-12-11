# cli.py

import json
import subprocess
import os
import logging
from multiprocessing import Pool

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def run_docker_image(image_config, output_directory, completed_images):
    try:
        image_id = image_config.get("id")

        # Check if the image has already been completed
        if image_id in completed_images:
            logging.info(f"{image_id} already completed.")
            return

        cli_args = image_config.get("cli-args",)

        # Build the Docker command
        docker_command = ["docker", "run", "--rm"]

        # Add the command line args
        docker_command.extend(cli_args)

        # Run the Docker image
        returncode = subprocess.run(docker_command, check=True).returncode

        if returncode == 0:
            completed_images.add(image_id)
            with open("completed_images.txt", "a") as completed_file:
                completed_file.write(f"{image_id}\n")

    except Exception as e:
        logging.error(f"Error running {image_id}: {str(e)}")

# find and replace all placeholders with the values
def replace_json_placeholders(json_str, values):
    for k, v in values.items():
        try:
            placeholder = "<%s>" % k
            json_str = json_str.replace(placeholder, v)
        except Exception as e:
            logging.warning(f"Failed to find and replace any placeholders with value {k} in config file")

    return json_str

# Updated to accept config_file as a parameter
def run_docker_images_main(config_file):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        placeholders = config.get("placeholders")

        with open(config_file, "r") as f:
            config_string = f.read()

        config_string = replace_json_placeholders(config_string, placeholders)
        config = json.loads(config_string)

        images = config.get("images", [])
        output_directory = config['values']['output_directory']

        # Load the list of completed images
        completed_images = set()
        if os.path.isfile("completed_images.txt"):
            with open("completed_images.txt", "r") as completed_file:
                completed_images = set(completed_file.read().splitlines())

        # Create a Pool to run Docker images in parallel
        pool = Pool(processes=config['values']['parallel_limit'])
        pool.starmap(run_docker_image, [(image, output_directory, completed_images) for image in images])
        pool.close()
        pool.join()

    except FileNotFoundError:
        logging.error(f"Config file '{config_file}' not found.")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in '{config_file}'.")
