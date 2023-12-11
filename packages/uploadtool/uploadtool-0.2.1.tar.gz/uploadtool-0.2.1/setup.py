#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
    name='uploadtool',
    version='0.2.1',
    description='python uploadtool for convenient.<Windows Only>',
    author_email='2229066748@qq.com',
    maintainer="Eagle'sBaby",
    maintainer_email='2229066748@qq.com',
    packages=find_packages(),
    license='Apache Licence 2.0',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords=['pypi', 'upload', 'twine'],
    python_requires='>=3',
    install_requires=[
        "twine",
        'wheel',
    ],
)
