from setuptools import find_packages, setup
import os
import shutil

setup(
    name='unix2app',
    version='0.0.1',
    packages=find_packages(include=['unix2app']),
    include_package_data=True,
    zip_safe=False,
    platform="any",
    # packages=['package1', 'package2', 'package3'],
    # package_dir={
    #     'package2': 'package1',
    #     'package3': 'package1',
    # },
    install_requires=[
        'Click==7.1.2',
        'PyYAML==5.3.1'
    ],
    entry_points={
        'console_scripts': [
            'unix2app=unix2app.unix2app:main'
        ]
    },
)
