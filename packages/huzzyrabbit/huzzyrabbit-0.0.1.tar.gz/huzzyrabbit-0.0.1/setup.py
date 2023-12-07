import setuptools
from pathlib import Path

setuptools.setup(
    name="huzzyrabbit",
    version="0.0.1",
    packages=setuptools.find_packages(exclude=["tests", "data"]),
    description="Huzzy Rabbit",
    long_description=Path("README.md").read_text(),
    author="Huzzy",
)