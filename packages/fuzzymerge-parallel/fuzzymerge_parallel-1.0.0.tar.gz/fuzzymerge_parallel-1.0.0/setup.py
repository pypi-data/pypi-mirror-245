#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

# try:
#     import pypandoc
#     long_description = pypandoc.convert_file('README.md', 'rst')
# except(IOError, ImportError):
#     long_description = open('README.md').read()

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'Levenshtein>=0.21.0', 'nltk>=3.8.1',
                'numpy>=1.23.5', 'pandas>=1.5.3', 'tqdm>=4.65.0', 'psutil==5.9.5']

test_requirements = ['pytest>=7.4.1', ]



setup(
    author="Oscar J. Castro-Lopez",
    author_email='oscar.castro@uni.lu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="FuzzyMergeParallel is a Python package that enables efficient fuzzy merging of two dataframes based on string columns. With FuzzyMergeParallel, users can easily merge datasets, benefitting from enhanced performance through parallel computing with multiprocessing and Dask.",
    entry_points={
        'console_scripts': [
            'fuzzymerge_parallel=fuzzymerge_parallel.cli:main',
        ],
    },
    install_requires=requirements,
    extras_require={
        "dask": ["dask[distributed]>=2023.5.0"],
    },
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='fuzzymerge_parallel',
    name='fuzzymerge_parallel',
    packages=find_packages(
        include=['fuzzymerge_parallel', 'fuzzymerge_parallel.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ULHPC/fuzzymerge_parallel',
    version='1.0.0',
    zip_safe=False,
)
