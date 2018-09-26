#!/usr/bin/env python
from setuptools import setup


setup(
    name="hyperdjango",
    version="0.0.0",
    author='Ross Fenning',
    author_email='github@rossfenning.co.uk',
    description='hyperdjango',
    url='http://github.com/avengerpenguin/hyperdjango',
    install_requires=[],
    setup_requires=['pytest-runner',],
    tests_require=['pytest', 'pytest-cov', 'pytest-xdist'],
    packages=['hyperdjango'],
)
