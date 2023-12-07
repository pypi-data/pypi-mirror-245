from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="horatio",
    version="0.1.6",
    author="Federico Sossai",
    author_email="federico.sossai@gmail.com",
    url="http://github.com/fsossai/horatio",
    description="Time your python scripts easily and with style",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["fslog"]
)
