from setuptools import setup, find_packages

VERSION = '0.0.22'
DESCRIPTION = 'Utilies module for r0p3 by r0p3'

setup(
    name="r0p3",
    version=VERSION,
    author="r0p3",
    author_email="<robin.pettersson.96@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['selenium', 'pytz', 'kubernetes', 'requests', 'beautifulsoup4', 'lxml', 'dataclasses', 'python-dateutil', 'pytz', 'tzlocal', 'pytzda'],
    keywords=['r0p3'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)