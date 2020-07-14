import setuptools

# Load README
with open("../README.md") as readmeFile:
    long_description = readmeFile.read()

setuptools.setup(
    name = "IAT_PRODER",
    version = "0.1",
    author = "Pablo Reyes Moctezuma",
    author_email = "pablo.reyes.moctezuma@gmail.com",
    description = "A lightweight IAT for measeuring stereotypes on skin tone",
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages = ["IAT"],
    package_dir = {
        "IAT": "."
    }
)