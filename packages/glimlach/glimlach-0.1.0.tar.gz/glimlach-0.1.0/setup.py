from setuptools import setup, find_packages

setup(
    name='glimlach',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python>=3.6',
        'docker>=4.4.4'
    ],
)
