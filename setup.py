#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="prowler",
    version='0.0.1',
    packages=find_packages(),
    author="rvanderp3",
    entry_points={
        "console_scripts": ["prowler=prowler.prowler:main"]
    },
    description="Provide a quick method of extracting prow data and logs for analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="",
    url="https://github.com/rvanderp3/prow-adapter",
    install_requires=[
        "pyyaml",
    ],
)