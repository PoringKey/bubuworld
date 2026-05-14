"""Setup configuration for funckey library."""

from setuptools import setup, find_packages

with open("funckey/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="funckey",
    version="0.1.0",
    author="PoringKey",
    description="A Python library for standard statistical functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PoringKey/bubuworld",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="statistics math functions library",
)
