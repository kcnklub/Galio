from setuptools import setup, find_packages

from lol_api import *

setup(
    name='lol_api',
    packages=find_packages(),
    author='Kyle Miller',
    description='Python wrapper for using riot games league of legends api',
    long_description=open('README.md').read(),
    url='https://github.com/kcnklub/lol-api.py',
    license='MIT',
    keywords='league, api, riot games',

    include_package_data=True
)