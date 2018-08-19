#!/usr/bin/env python

from setuptools import setup

setup(
  name="pchaps",
  version="1.0",
  py_modules=["pchaps", "chaps_lib"],
  install_requires=["Click", "sarge", ],
  entry_points={
    "console_scripts": ["pchaps=pchaps:cli"],
  }
)
