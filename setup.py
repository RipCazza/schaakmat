#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
]

test_requirements = [
]

setup(
    name='schaakmat',
    version='0.0.1',
    description='Schaakmat is a chess engine.',
    long_description=readme + '\n\n' + history,
    author='Ruben Bakker',
    author_email='rubykuby@gmail.com',
    url='https://github.com/Rubykuby/schaakmat',
    packages=[
        'schaakmat',
    ],
    package_dir={'schaakmat':
                 'schaakmat'},
    include_package_data=True,
    install_requires=requirements,
    license="LGPLv3+",
    zip_safe=False,
    keywords='schaakmat',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
