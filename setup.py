#!/usr/bin/env python3
import os
from setuptools import find_packages, setup

SETUP_DIR = os.path.dirname(__file__)
README = os.path.join(SETUP_DIR, 'README.md')

setup(
    name='datameta_client',
    version='0.0.1',    
    description='A high-level client for interacting with a DataMeta service',
    long_description=open(README).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/ghga-de/datameta-client',
    download_url="https://github.com/ghga-de/datameta-client",
    author='Kersten Henrik Breuer',
    author_email='k.breuer@dkfz.de',
    license='Apache 2.0',
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "datameta_client=datameta_client.__main__:app",
        ]
    },
    install_requires=[
        'typer',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha  ',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry ',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX', 
        'Operating System :: POSIX :: Linux',    
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows', 
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ]
)