import os
from setuptools import setup, find_packages

local_file = lambda f: open(os.path.join(os.path.dirname(__file__), f)).read()

if __name__ == '__main__':
    setup(
        name='thegamesdb',
        version='0.2',
        description='The Games DB API wrapper for Python',
        long_description=local_file('README.md'),
        author='Rogerio Hilbert Lima',
        author_email='rogerhil@gmail.com',
        url='https://github.com/rogerhil/thegamesdb',
        download_url='https://github.com/rogerhil/thegamesdb/tarball/0.2',
        packages=find_packages()
    )
