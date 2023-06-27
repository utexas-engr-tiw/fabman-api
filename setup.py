import re
from distutils.core import setup
from os import path

# get version number from fabman/__init__.py
with open("fabman/__init__.py") as f:
    version = re.search(r"__version__ = (.*)", f.read()).group(1)

setup(
    name="Fabman API",
    version=version,
    description="Library for interfacing with the Fabman API",
    author="Davin Lawrence",
    author_email="fabman-api@tinycact.us",
    packages=["fabman"],
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
    ],
)
