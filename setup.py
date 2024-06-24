from setuptools import setup, find_packages

setup(
   name='PySOMVis',
   version='0.0.1',
   author='Sergei Mnishko',
   author_email='sergei.mnishko@gmail.com',
   packages=['PySOMVis'],
   url='https://github.com/smnishko/PySOMVis',
   license='LICENSE.txt',
   description='PySOMVis is an open-source Python-based GUI implementation for analyzing trained SOMs. It provides a wide range of different visualizations for the SOM, such as Chessboard Visualization, Clustering approach, Component Plane, D-Matrix, Hit Histogram, Metro Map, Neighborhood Graphs, Pie Chart, Smoothed Data Histogram, U-Matrix, U*-Matrix, P-Matrix, Quantization Error, SOMStreamVis',
   long_description=open('README.md').read(),
   install_requires=[
        'bokeh>=2.4.1',
        'holoviews>=1.14.8',
        'numpy>=1.20.3',
        'pandas>=1.3.4',
        'panel>=0.13.0',
        'param>=1.12.1',
        'scikit_image>=0.18.3',
        'scikit_learn>=1.0.2',
        'scipy>=1.7.1'],
)
