#!/usr/bin/python
# coding: utf8

from codecs import open
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('geocoder/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

requires = ['requests', 'ratelim', 'click', 'six', 'future']

setup(
    name='geocoder-compensa',
    version=version,
    description="Geocoder is a simple and consistent geocoding library.",
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Denis Carriere',
    author_email='carriere.denis@gmail.com',
    url='https://github.com/compensa-eco/geocoder-compensa',
    download_url='https://github.com/compensa-eco/geocoder-compensa',
    license="The MIT License",
    entry_points='''
        [console_scripts]
        geocode=geocoder.cli:cli
    ''',
    packages=['geocoder'],
    package_data={'': ['LICENSE', 'README.md']},
    package_dir={'geocoder': 'geocoder'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    keywords='geocoder arcgis tomtom opencage google bing here',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
