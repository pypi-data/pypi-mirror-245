# setup.py

from setuptools import setup, find_packages

setup(
    name='simple_calculator_2023',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        # Any dependencies your project may have
    ],
    entry_points={
        'console_scripts': [
            'calculator = calculator.calculator:main',
        ],
    },
)
