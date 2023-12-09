from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'Learn to create python package'
LONG_DESCRIPTION = 'A package that allows to play guess number game and converting weight unit'

# Setting up
setup(
    name="GuessConversionPkg",
    version=VERSION,
    author="Himm (Ibrahim Aryan Faridzi)",
    author_email="<ibra12@test.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'guess', 'number', 'weight', 'conversion', 'guess number', 'weight conversion'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
