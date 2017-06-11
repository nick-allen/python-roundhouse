#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()


with open('README.rst') as readme_file:
    README = readme_file.read()

setup(
    name='roundhouse',
    description="Convert many serialization formats to many formats",
    long_description=README,
    author="Nick Allen",
    author_email='nick.allen.cse@gmail.com',
    url='https://github.com/nick-allen/roundhouse',
    packages=find_packages(include=['roundhouse']),
    setup_requires=[
        'setuptools_scm',
        'pytest-runner'
    ],
    use_scm_version=True,
    entry_points={
        'console_scripts': [
            'roundhouse=roundhouse.cli:main'
        ],
        'roundhouse': [
            'contrib_serializers=roundhouse.contrib.serializers'
        ]
    },
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    license="MIT license",
    zip_safe=False,
    keywords='roundhouse',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=parse_requirements('test-requirements.txt')
)
