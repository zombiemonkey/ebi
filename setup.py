# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='ebi',
    version='0.5.0',
    description='Indempotent task execution system build on SaltStack',
    author='Jason Godden',
    author_email='jason@godden.id.au',
    maintainer='Jason Godden',
    maintainer_email='jason@godden.id.au',
    license='Apache',
    zip_safe=False,
    package_dir={
        'ebi':'ebi',
    },
    packages=[
        'ebi'
        'ebi.cli'
    ],
    entry_points={
        'console_scripts': [
            'ebi = ebi.scripts:ebi_cli'
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.6",
        "Topic :: System",
        "Topic :: Utilities",
    ],
)
