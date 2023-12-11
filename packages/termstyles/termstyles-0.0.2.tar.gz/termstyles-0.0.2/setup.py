from setuptools import setup, find_packages
import codecs
import os

with open('termstyles/README.md', 'r', encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Simple terminal coloring module'
LONG_DESCRIPTION = 'Simple terminal coloring module. Using termstyles you can write colored output to the terminal'

# Setting up
setup(
    name="termstyles",
    version=VERSION,
    author="N0NL0C4L",
    author_email="<n0nl0c4l@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'color', 'termstyles', 'terminal', 'console'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
