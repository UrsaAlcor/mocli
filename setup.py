#!/usr/bin/env python
from setuptools import setup


if __name__ == '__main__':
    setup(
        name='mocli',
        version='0.0.0',
        description='Lmod command line interface for managing its installation ',
        author='Pierre Delaunay',
        packages=[
            'mocli',
            'mocli.cmd'
        ],
        setup_requires=['setuptools'],
        install_requires=['appdirs'],
            entry_points={
            'console_scripts': [
                'alcor = mocli.cli:main',
            ]
        },
        package_data={
            "mocli": [
                'mocli/cmd/templates/ModuleFile.lua'
            ]
        },
    )
