#!/usr/bin/env python

import pathlib
import setuptools
import sys

topdir = pathlib.Path(__file__).parent


def readfile(f):
    return (topdir / f).read_text("utf-8").strip()


extra_options = {}

if sys.version_info.major == 3 and sys.version_info.minor >= 7:
    extra_options["long_description_content_type"] = "text/markdown"

setuptools.setup(
    name="asyncio-datagram",
    version="1.4.0",
    description="Higher level Datagram support for Asyncio",
    long_description=readfile("README.md"),
    url="https://github.com/mishamyrt/asyncio-datagram",
    author="Mikhael Khrustik",
    author_email="misha@myrt.co",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_data={"asyncio_datagram": ["*.pyi", "py.typed"]},
    include_package_data=True,
    packages=["asyncio_datagram"],
    python_requires=">=3.6",
    install_requires=readfile("requirements.txt").split(),
    extras_require={"test": readfile("requirements-test.txt").split()},
    **extra_options,
)
