import pathlib
from setuptools import setup, find_packages

setup(
    name="cryptonid",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Bency Dsouza",
    description="A simple encryption method",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)