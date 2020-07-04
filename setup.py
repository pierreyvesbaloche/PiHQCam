# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pihqcam',
    version='0.1.0',
    description='Python package for the Raspberry Pi Project PiHQCam',
    long_description=readme,
    author='Pierre-yves Baloche',
    author_email='funkypiwy@gmail.com',
    url='https://github.com/pierreyvesbaloche/PiHQCam',
    license=license,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=find_packages(exclude=('tests', 'docs'))
)