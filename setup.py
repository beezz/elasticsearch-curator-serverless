from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read()


setup(
    name='elasticsearch-curator-serverless',
    version=version,
    description='Elasticsearch curator serverless handler',
    long_description=long_description,
    url='https://github.com/beezz/elasticsearch-curator-serverless',
    author='Michal Kuffa',
    author_email='michal.kuffa@gmail.com',
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=['elasticsearch-curator>=5.2', 'requests'],
)
