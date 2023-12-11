from setuptools import setup, find_packages

setup(
    name='glimlach',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'docker>=4.4.4'
    ],
     entry_points={
        'console_scripts': [
            'run-docker-images = cli:run_docker_images_main',
        ],
    },
)
