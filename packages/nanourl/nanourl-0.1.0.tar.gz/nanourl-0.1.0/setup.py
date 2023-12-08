from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='nanourl',
    version='0.1.0',
    packages=find_packages(include=['url_shortener.py', 'main.py']),
    long_description=long_description,
    long_description_content_type='text/markdown',
)