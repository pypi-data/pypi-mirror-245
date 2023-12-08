import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '3.7.1'
PACKAGE_NAME = 'nazca4sdk'
AUTHOR = 'You'
AUTHOR_EMAIL = 'you@email.com'
# URL = 'https://github.com/you/your_package'


LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Describe your package in one sentence'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
with open('requirements.txt') as f:
    required = f.read().splitlines()

INSTALL_REQUIRES = required

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      # url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )