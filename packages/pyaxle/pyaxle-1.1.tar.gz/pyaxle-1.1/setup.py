from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

setup(
    name="pyaxle",
    version="1.1",
    packages=find_packages(),
    # There are no dependencies for pyaxle
    # as of now
    long_description=long_description,
    long_description_content_type='text/markdown'
)