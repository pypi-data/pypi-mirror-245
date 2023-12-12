from setuptools import setup,find_packages
from distutils.core import setup
from pathlib import Path
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='ranshark',
    version='1.0.0.4',
    description='A friendly 5g o-ran packet analyzing tool with GUI interface.',
    license="Apache-2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ugandhar',
    author_email='ugandhar.nellore@gmail.com',
    keywords=['ran', '5g', '5g analyzer', 'ranshark'],

    classifiers=[
        "Intended Audience :: Telecommunications Industry",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3.10",
    ],

        install_requires=[
        'Django~=4.2.7',
        'celery~=5.3.4',
        'pandas~=1.3.3',
        'pyshark~=0.6',
        'psycopg2==2.9.9',
        'psycopg2-binary==2.9.9',

    ],
    include_package_data = True,
    )
