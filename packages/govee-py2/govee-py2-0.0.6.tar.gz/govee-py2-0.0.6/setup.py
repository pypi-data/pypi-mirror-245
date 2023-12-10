from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.6'
DESCRIPTION = 'Interacting with Govee Lights via Python'
LONG_DESCRIPTION = 'A package that allows light device interaction with Govee API 2.0 using Python'

# Setting up
setup(
    long_description_content_type="text/markdown",
    long_description=long_description,
    name="govee-py2",
    version=VERSION,
    author="Sxzo",
    author_email="",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'subprocess'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)