"""Setup configuration for digital_clock package."""

from setuptools import setup, find_packages

with open("digital_clock/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="digital-clock",
    version="1.0.0",
    author="PoringKey",
    description="Digital clock that displays current time in multiple time zones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PoringKey/bubuworld",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    keywords="clock timezone time display",
)
