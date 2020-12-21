# -*- coding: utf-8 -*-
"""
setup.py script
"""

import io
from collections import OrderedDict
from setuptools import setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    README = f.read()

setup(
    name='dojot.module.healthcheck',
    version='0.1.0',
    url='http://github.com/dojot/healthcheck-python',
    project_urls=OrderedDict((
        ('Code', 'https://github.com/dojot/healthcheck-python.git'),
        ('Issue tracker', 'https://github.com/dojot/healthcheck-python/issues'),
    )),
    license='Apache-2.0',
    author='Giovanni Curiel dos Santos',
    author_email='giovannicuriel@gmail.com',
    maintainer='dojot team',
    description='Healthcheck library for dojot modules development',
    long_description=README,
    packages=["dojot.module.healthcheck"],
    include_package_data=True,
    zip_safe=False,
    platforms=[any],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'marshmallow==3.0.0b8'
    ],
    extras_require={
        "dev": [
            "pytest==4.0.0",
            "pytest-cov==2.6.0"
        ]
    }
)
