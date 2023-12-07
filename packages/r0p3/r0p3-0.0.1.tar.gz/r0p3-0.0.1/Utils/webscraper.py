from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Utilies module for r0p3 by r0p3'
LONG_DESCRIPTION = 'What description just said'

# Setting up
setup(
    name="r0p3",
    version=VERSION,
    author="r0p3",
    author_email="<robin.pettersson.96@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['selenium',],
    keywords=['r0p3'],
    classifiers=[
        "No"
    ]
)