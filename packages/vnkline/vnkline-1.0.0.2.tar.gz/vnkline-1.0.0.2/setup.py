from setuptools import setup, find_packages, Distribution
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

setup(
    name='vnkline',  # Required
    version='1.0.0.2',  # Required
    description='vnkline',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://gitee.com/vnpypro/vnkline',  # Optional
    license = 'https://gitee.com/vnpypro/vnklineservice/blob/master/LICENSE',
    author='quant lin',  # Optional
    author_email='1196999641@qq.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
      
    ],
    keywords='barcode DataMatrix QRCode 1D PDF417',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=['numpy', 'pandas','pyqtgraph','PyQt5'],


   package_data={  # Optional
        'kline': ['vnklineservice.dll', 'zlibwapi.dll','libcurl.dll','libeay32.dll', 'ssleay32.dll', 'vnklineservice.ini']},

data_files=[
    ('bitmaps', ['vnkline/vnklineservice.dll', 'vnkline/zlibwapi.dll','vnkline/libcurl.dll','vnkline/libeay32.dll', 'vnkline/ssleay32.dll', 'vnkline/vnklineservice.ini'])

])