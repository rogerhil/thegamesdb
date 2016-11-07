import os
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

local_file = lambda f: open(os.path.join(os.path.dirname(__file__), f)).read()

if __name__ == '__main__':
    setup(
        name='thegamesdb',
        version='0.7',
        description='The Games DB API wrapper for Python',
        long_description=long_description,
        author='Rogerio Hilbert Lima',
        author_email='rogerhil@gmail.com',
        url='https://github.com/rogerhil/thegamesdb',
        download_url='https://github.com/rogerhil/thegamesdb/tarball/0.7',
        packages=find_packages()
    )
