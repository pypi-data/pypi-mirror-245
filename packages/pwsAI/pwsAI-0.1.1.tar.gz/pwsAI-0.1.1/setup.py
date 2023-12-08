
# -*- coding: utf-8 -*-
"""
This file is used to install the pwsAI package. for example navigate in your terminal to the directory containing this
file and type `pip install .`.
"""
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent  # The directory containing this file
README = (HERE / "README.md").read_text()  # The text of the README file

setup(name='pwsAI',
      version='0.1.1',
      description='A GUI for AI segmentation of cell imagery.',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Nico Acosta',
      author_email='nicolasacosta2026@u.northwestern.edu',
      url='https://github.com/nanthony21/pws_AI',
      python_requires='>=3.6',
      install_requires=['numpy',
                        'matplotlib',
                        'PySimpleGUI',
                        'pwspy',
                        'pillow',
                        'scikit-image',
                        'scikit-learn',
                        'tifffile',
                        'opencv-python',
                        'patchify',
                        'h5py',
                        'rasterio',
                        'tensorflow'
                        ],
      package_dir={'': 'src'},
      package_data={'pwsAI': ['_resources/*']},
      packages=find_packages('src'),
	  entry_points={'gui_scripts': [
          'PwsAIGui = pwsAI.__main__:main'
      ]}
	)
