#!/bin/python3

import warnings
import os
from setuptools import setup, find_packages

__version__ = None
exec(open('HiCShuffle/version.py').read())

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
  name = 'HiCShuffle',
  packages = ['HiCShuffle'],
  version = __version__,
  license='MIT',
  description = 'FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis',
  long_description=read_file('README.md'),
  long_description_content_type='text/markdown',
  author = 'Hanjun Lee',
  author_email = 'hanjun@mit.edu',
  url = 'https://github.com/hanjunlee21/HiCShuffle',
  download_url = 'https://github.com/hanjunlee21/HiCShuffle/archive/refs/tags/v.' + __version__ + '.tar.gz',
  keywords = ['hi-c', 'qc'],   
  install_requires=[
          'numpy',
          'argparse',
      ],
  scripts=['bin/hicshuffle'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Science/Research',      
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Awk',
    'Programming Language :: Unix Shell',
  ],
)
