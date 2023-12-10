from setuptools import setup
from habitica import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="py-habitica",
    version=__version__,
    author="skifli",
    url="https://github.com/ankitica/py-habitica",
    project_urls={
        "Documentation": "https://github.com/ankitica/py-habitica",
        "Source": "https://github.com/ankitica/py-habitica",
    },
    description="An API wrapper for Habitica's API, in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=["habitica"],
)
