import setuptools
from pathlib import Path

setuptools.setup(
    name="moshpdforietta",
    # unique name that doesn't conflict with another one in Pypi repository
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]),
    # modules & packages going to publish
    # find_packages() will automatically discover packages we have defined in project
    # but need to tell the exclude directories "test" & "data"
)