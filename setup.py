from setuptools import setup, find_packages

from lol_api import *

setup(
    name='lol_api',
    packages=find_packages(),
    author='Kyle Miller',
    description='Python wrapper for using riot games league of legends api',
    long_description=open('README.md').read(),
    include_package_data=True
)