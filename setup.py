#!/usr/bin/env python
from setuptools import setup


deps = [
    'django', 'inflect', 'rdflib', 'rdflib-jsonld',
    'flask_rdf', 'pyld', 'yarl',
]
test_deps = [
    'pytest-django', 'pytest-env', 'django12factor', 'pylama', 'laconia',
]


setup(
    name="hyperdjango",
    version="0.0.0",
    author='Ross Fenning',
    author_email='github@rossfenning.co.uk',
    description='hyperdjango',
    url='http://github.com/avengerpenguin/hyperdjango',
    install_requires=deps,
    tests_require=test_deps,
    extras_require={'test': test_deps},
    packages=['hyperdjango'],
)
