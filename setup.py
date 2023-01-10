#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='nogging',
    version='1.1.0',
    description='Automatically use `nogging.yaml` to manage loggers.',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.0',
    url='https://github.com/my-python-utils/nogging',
    packages=[
        'nogging',
    ],
    install_requires=[
        'pyyaml',
    ],
    license='MIT License',
)
