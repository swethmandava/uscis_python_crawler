import setuptools
import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="uscis_python_crawler",
    version="0.0.1",
    author="Swetha Mandava",
    author_email="sweth.mandava@gmail.com",
    description="USCIS Python Crawler",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)