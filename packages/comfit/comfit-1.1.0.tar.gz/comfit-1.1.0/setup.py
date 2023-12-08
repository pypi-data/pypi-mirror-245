from setuptools import setup

setup(
    name='comfit',
    version='1.1.0',
    packages=['comfit'],
    package_data={'comfit':['core/*','models/*','tools/*']},
    author='Vidar Skogvoll and Jonas Rønning',
    install_requires=['numpy>=1.22.0','scikit-image','matplotlib','moviepy==1.0.3','imageio'],
)