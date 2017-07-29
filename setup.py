from setuptools import setup, find_packages

from Galio import *

setup(
    name='Galio',
    version='1.0.0',
    packages=find_packages(),
    author='Kyle Miller',
    author_email='kylemiller457@gmail.com',
    description='Python wrapper for using riot games league of legends api',
    long_description=open('README.md').read(),
    url='https://github.com/kcnklub/lol-api.py',
    license='MIT',
    keywords='league, api, riot games',
    python_requires='>=3',
    include_package_data=True,
    classifiers=[]
)