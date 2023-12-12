from setuptools import setup, find_packages

setup(
    name="NUTT",
    version="0.0.5",
    packages=find_packages(),
    description="A custom machine learning library",
    author="Simon Slamka",
    author_email="simon.slamka@ongakken.com",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/simonSlamka/NUTT",
    install_requires=["termcolor"]
)