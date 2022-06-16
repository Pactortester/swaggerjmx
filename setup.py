#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from swaggerjmx import __version__

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="swaggerjmx",
    version=__version__,
    keywords=["pip", "swagger", "jmx", "yapi", "swaggerjmx", "jmeter", "swagger convert jmx"],
    description="swagger convert jmx",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",

    url="https://github.com/Pactortester/swaggerjmx",
    author="lijiawei",
    author_email="1456470136@qq.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console :: Curses",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
        "Typing :: Typed",
    ],
    entry_points="""
    [console_scripts]
    swaggerjmx = swaggerjmx.cli:main
    """,
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["lxml", "requests", "loguru"]
)
