#!/usr/bin/env python3
#
# Copyright 2021 Universität Tübingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools import find_packages, setup

SETUP_DIR = os.path.dirname(__file__)
README = os.path.join(SETUP_DIR, 'README.md')

version = '1.0.0'
major_version = int(version.split(".")[0])

setup(
    name                           = 'datameta_client',
    version                        = version,
    packages                       = find_packages(),
    description                    = 'A high-level client for interacting with a DataMeta service',
    long_description               = open(README).read(),
    long_description_content_type  = "text/markdown",
    url                            = 'https://github.com/ghga-de/datameta-client',
    download_url                   = "https://github.com/ghga-de/datameta-client",
    author                         = 'Kersten Henrik Breuer',
    author_email                   = 'k.breuer@dkfz.de',
    license                        = 'Apache 2.0',
    include_package_data           = True,
    entry_points={
        "console_scripts": [
            "dmclient=datameta_client.__main__:app",
        ]
    },
    install_requires=[
        'typer',
        f'datameta-client-lib>=1.0.1,<{major_version+1}',
        'pyyaml',
        'requests',
    ],
    extras_require={
        'testing': [
            'pytest',
            'pytest-cov'
        ],
    },
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
