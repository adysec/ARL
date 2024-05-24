#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

from xing import __version__ as version

setuptools.setup(
    name="xing",
    version=version,
    author="ice.liao",
    author_email="ice.liao@tophant.com",
    description="Yet Another PoC Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.tophant.com/Sec/NPoC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "xing=xing.main:main"
        ]
    }
)