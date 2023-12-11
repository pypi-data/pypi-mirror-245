from setuptools import setup, find_packages

setup(
    name='glimlach',
    version='0.4.7',
    description='Glimlach is a project that allows you to easily run Docker images based on a configuration file.',
    long_description='''\
   Glimlach is a cybersecurity automation tool designed to streamline the execution of multiple open-source security tools in a single scan. The project is initiated to support Rauli's research, enabling automated complex security scans with commonly used tools like Nmap, Testssl.sh, and Ssh-audit. This tool is a Python script that allows you to run Docker tools in parallel based on a JSON configuration file. It is designed to make it easy to automate the execution of Docker images with customizable parameters.

The primary objective is to facilitate the execution of various cybersecurity tools as a single scan without the need for individual installations and configurations. Glimlach focuses on the containerized execution (OCI) of tools, allowing for isolation and reproducibility.
    ''',
    author="'Emmanuel Ikwunna', 'Arttu Juntunen', 'Piyumi Weebadu Arachchige'",
    url='https://github.com/firstnuel/Glimlach',
    packages=find_packages(),
    install_requires=[
        'docker>=4.4.4'
    ],
     entry_points={
        'console_scripts': [
            'glimlach = glimlach.__main__:main',
        ],
    },
)