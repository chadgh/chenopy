#!/usr/bin/env python
from distutils.core import setup

setup(name='Chenopy',
      version='1.0',
      description='Chess notation parsing tools.',
      author='Chad G. Hansen',
      author_email='chadgh@gmail.com',
      url='https://github.com/chadgh/chenopy',
      packages=['chenopy', 'chenopy.tests'],
      license='Creative Commons Attribution-Noncommercial-Share Alike license',
      long_description=open('README').read(),
      tests_require=['coverage==3.7.1', 'nose==1.3.0'],
      include_package_data=True,
      )
