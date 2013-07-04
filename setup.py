import os
from setuptools import setup, find_packages

requires = [
    'Flask',
    'Flask-KVSession',
    'Flask-WTF',
    'pillow', # As PIL is not incompatible with setuptools, look for an alternative
    'simple-pbkdf2',
    'cmd2',
]

entry_points = {
    'console_scripts': [
        'dahu-cli = dahu.cli.dahu_cli:main',
        'dahu-web = dahu.frontend.dahu_web:main'
    ]
}



version = '0.1.0'
README = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(README).read()

setup(
    name='dahu',
    version=version,
    description=("A Flask-based web gallery using no database"),
    long_description=long_description,
    author='Damien Riquet',
    author_email='d.riquet@gmail.com',
    url='https://github.com/driquet/dahu',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['dahu'],
    install_requires=requires,
    entry_points = entry_points,
)
