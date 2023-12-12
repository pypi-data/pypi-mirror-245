#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/13 10:28
# @Author  : jw
from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(name='jw_ws',  # 包名
      version='1.1.2',  # 版本号
      description='A small based on websocket',
      long_description="",
      author='jw',
      author_email='jw19961019@gmail.com',
      url='https://github.com/CodingJzy',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries'
      ],
      python_requires='>=3.6',  # 对python的最低版本要求
      )
