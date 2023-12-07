#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='tokenizers_pegasus',
    version='0.0.4',
    author='xiaoql',
    author_email='xiaoql@gmail.com',
    url='https://github.com/Qiliang/pegasus.git',
    description=u'tokenizers for pegasus',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['jieba', 'rouge',
                      'torch', 'numpy', 'six'],
    entry_points={}
)
