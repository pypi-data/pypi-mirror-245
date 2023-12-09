#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from distutils.core import setup
setup(
  name = 'cdg_reader',
  packages = ['cdg_reader'],
  version = '0.5',
  license='MIT',
  description = 'Check the NCAR Climate Data Guide for information relevant to your netCDF data file',
  author = 'YDylan Grant',
  author_email = 'dg3311@columbia.edu',
  url = 'https://github.com/dylangrant01/cdg-reader',
  download_url = 'https://github.com/dylangrant01/cdg-reader/archive/refs/tags/v05.tar.gz',
  keywords = ['ncar', 'cdg', 'climate', 'guide', 'xarray'],
  install_requires=[            
          'xarray',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)