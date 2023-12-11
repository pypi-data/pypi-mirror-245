import requests
import setuptools
from setuptools import setup, find_packages

setup(
    name='dialoget',
    version='0.0.1',
    author='Tom Sapletta',
    author_email='tom@sapletta.com',
    packages=find_packages(),
    license='LICENSE',
    description='A Sentence decorator for dynamic log messages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests >= 2',
        'setuptools >= 67.7.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)