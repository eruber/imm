#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pillow'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='imm',
    version='2.1.0',
    description="Image Module Maker",
    long_description="A library & command line utility for processing image files & embedding them into a Python module",
    author="E.R. Uber",
    author_email='eruber@gmail.com',
    url='https://github.com/eruber/imm',
    packages=[
        'imm',
    ],
    py_modules = ['immcli'],
    package_dir={'imm':
                 'imm'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='imm',
    entry_points={
        'console_scripts': [
            'imm = immcli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
