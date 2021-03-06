import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="magellan-catalog",
    version="0.0.0",
    author="Zack Klein",
    author_email="klein.zachary.j@gmail.com",
    description=(
        "A simple but powerful Data Catalog built on top of Flask, "
        "Elasticsearch, and pandas."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zack-klein/magellan",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["magellan=magellan.cli:main"]},
    install_requires=requirements,
    python_requires=">=3.6",
)
