"""
-*- coding: utf-8 -*-
@Time : 2023/4/14 9:46
"""
from setuptools import setup

setup(
    name='my_package',
    version='1.0',
    packages=['my_package'],
    install_requires=[
        "os",
        "PyPDF2"
    ],
    entry_points={
        'console_scripts': [
            'my_script = my_package.my_script:main',
        ],
    },

)