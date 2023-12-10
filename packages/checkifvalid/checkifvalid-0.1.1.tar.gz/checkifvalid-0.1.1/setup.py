#!/usr/bin/python

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

KEYWORDS = ('ipv6 ipv4 syntax validator regex')

setuptools.setup(
    name="checkifvalid",
    version="0.1.1",
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="Syntax validator for email, hostname, url, uri and ip address, compliant to RFC specifications ",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dmachard/python-checkifvalid",
    packages=['checkifvalid', 'tests'],
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ]
)