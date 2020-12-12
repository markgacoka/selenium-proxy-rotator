import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium-proxy-rotator",
    version="0.0.2",
    author="Gacoka Mbui",
    author_email="markgacoka@gmail.com",
    description="A python wrapper around selenium that makes web automation anonymous through elite proxy rotation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markgacoka/selenium-proxy-rotator",
    packages=setuptools.find_packages()
)