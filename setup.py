from setuptools import setup
from setuptools import find_packages


setup(
    name='google-doubleclick-decrypter',
    url='https://github.com/trein/google-doubleclick-decrypter/',
    version='1.0.0',
    author='Guilherme Trein',
    description='Google DoubleClick Ad Exchange RTB Decrypter',
    long_description='Google decrypter following DoubleClick Ad Exchange Real-Time Bidding Protocol',
    packages=find_packages(exclude=['tests']),
    package_dir={'google-doubleclick-decrypter': 'google-doubleclick-decrypter'},
)