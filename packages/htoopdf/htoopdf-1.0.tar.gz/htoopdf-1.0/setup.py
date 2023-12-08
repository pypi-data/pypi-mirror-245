import setuptools
from pathlib import Path


setuptools.setup(
    name="htoopdf",
    version=1.0,
    description=Path("README.md").read_text(),
    # find([the files where you don't want to look for packates])
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
