from setuptools import setup , find_packages
from pathlib import Path
this_directory = Path(__file__).parent
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.1',
    'Intended Audience :: Developers',
]

setup(
    name='MainOperations',
    version='0.0.1',
    description='A test Package for A/S/M/D 2 number',
    long_description=(this_directory / 'Readme.txt').read_text() + '\n\n' + (this_directory / 'Changelog.txt').read_text(),
    url='',
    author='Asghar Haghi',
    author_email='asghar.haghi@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Calculator',
    packages=find_packages(),
    
)
