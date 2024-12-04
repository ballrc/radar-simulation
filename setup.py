from setuptools import setup

setup(
    name="radar-simulation",
    version="0.0.0",
    author="Ryan Ball",
    description="A module for running radar simulations with configurable radar systems for signal processing algorithm effectiveness assessment.",
    url="https://github.com/ballrc/radar-simulation",
    python_requires=">=3.13.1",
    install_requires=[
        "numpy",
        "matplotlib"
    ]
)