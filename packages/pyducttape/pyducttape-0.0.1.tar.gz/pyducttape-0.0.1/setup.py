#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyducttape",
    version="0.0.1",
    description="Package, encrypt and obfuscate Python scripts",
    long_description=read("README.md"),
    author="Michael Williamson, Bintang Pradana Erlangga Putra",
    author_email="mike@zwobble.org, work.bpradana@gmail.com",
    url="https://github.com/bpradana/ducttape",
    packages=["ducttape"],
    install_requires=["astor", "PyCryptodome"],
    python_requires=">=3.5",
    license="BSD-2-Clause",
    entry_points={
        "console_scripts": [
            "ducttape=ducttape.main:main",
        ],
    },
)
