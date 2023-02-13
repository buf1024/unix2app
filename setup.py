from setuptools import find_packages, setup

with open("README.MD", "r") as f:
    long_description = f.read()

setup(
    name='unix2app',
    version='0.0.1',
    packages=find_packages(include=['unix2app']),
    include_package_data=True,
    zip_safe=False,
    description='Mac console ui to gui app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/buf1024/unix2app",
    platform="any",
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
