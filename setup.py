#!/usr/bin/env python
from setuptools import setup

NAME = "hyperdjango"


deps = [
    "django",
    "inflect",
    "rdflib",
    "rdflib-jsonld",
    "requests",
    "flask_rdf",
    "pyld",
    "yarl",
]
test_deps = [
    "pytest-django",
    "pytest-env",
    "django12factor",
    "pylama",
    "laconia",
    "hypothesis",
]

setup(
    name=NAME,
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": f"{NAME}/_version.py",
        "fallback_version": "0.0.0",
    },
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    description=NAME,
    url=f"https://github.com/avengerpenguin/{NAME}",
    install_requires=deps,
    tests_require=test_deps,
    extras_require={"test": test_deps},
    setup_requires=[
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    packages=[NAME],
)
