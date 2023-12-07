#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

from qatools import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="qatools",
    version=f"{__version__}",
    keywords=["utx", "adb", "qa", "tools"],
    description="QA is an advanced tool for Android testing!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://openutx.cn/",
    author="lijiawei",
    author_email="jiawei.li2@qq.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console :: Curses",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points="""
    [console_scripts]
    qa = qatools.qa:mode
    """,
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "psutil",
    ],
)
