#!/usr/bin/env python

"""Tests for `fuzzymerge_parallel` package."""

import pytest
from click.testing import CliRunner
# from nltk.corpus import movie_reviews
# import nltk
import pandas as pd
from fuzzymerge_parallel.FuzzyMergeParallel import FuzzyMergeParallel



def dask_is_installed() -> bool:
    """Checks if dask is installed. This is an auxiliary function to skip dask tests if it's not installed.

    Returns:
        bool: True if dask was imported succesfully, Otherwise False.
    """
    try:
        import dask
        library_installed = True
    except ImportError:
        library_installed = False
    return library_installed


pytest.mark.dask = pytest.mark.skipif(
    (not dask_is_installed()),
    reason="Test requires 'dask' extra to be installed."
)


@pytest.fixture(scope="module")
def dataset():
    """Loads a preprocessed subset of the NLTK corpora/movie_reviews dataset.

    This function loads a curated subset of 5000 rows from the corpora/movie_reviews dataset available in the NLTK package. The original dataset, which contains movie-review text data, was processed to create this subset for testing purposes.

    Dataset Source: [NLTK - Movie Reviews Corpus](http://www.cs.cornell.edu/people/pabo/movie-review-data/)

    The subset dataset has already been carefully filtered and tested with levenshtein distance for each pair, resulting in 600 matching records. Therefore, the expected shape of the yielded dataframes is (600, 2).

    Yields:
        pd.DataFrame: Two dataframes, each containing a list of words from preprocessed movie-review data.
    """
    words_left = pd.read_csv('tests/words_left.zip')
    words_right = pd.read_csv('tests/words_right.zip')
    yield words_left, words_right


def test_sequential(dataset):
    """Basic sequential text execution of FuzzyMergeParallel.
    """
    left_df, right_df = dataset
    fm_seq = FuzzyMergeParallel(
        left_df, right_df, left_on='words_left', right_on='words_right')
    # Set parameters
    fm_seq.set_parameter('how', 'inner')
    fm_seq.set_parameter('parallel', False)
    # Run the merge sequentially
    result = fm_seq.merge()
    assert result.shape == (600, 2)


def test_basic_multiprocessing(dataset):
    """Basic multiprocessing test execution of FuzzyMergeParallel.
    """
    left_df, right_df = dataset
    fm_multi = FuzzyMergeParallel(
        left_df, right_df, left_on='words_left', right_on='words_right')
    # Set parameters
    fm_multi.set_parameter('how', 'inner')
    # Set parameters for multiprocessing
    fm_multi.set_parameter('n_threads', 'all')  # All available cores
    # Run the merge multiprocessing
    result = fm_multi.merge()
    assert result.shape == (600, 2)


@pytest.mark.dask
def test_basic_dask(dataset):
    """Basic dask test execution of FuzzyMergeParallel.
    """
    from dask.distributed import Client, LocalCluster
    left_df, right_df = dataset
    # Create a local Dask cluster
    cluster = LocalCluster()
    # Create a Dask client to connect to the cluster
    client = Client(cluster)
    # Get the total number of cores available in the cluster
    total_cores = sum(client.ncores().values())
    print("total cores ", total_cores)
    fm_dask = FuzzyMergeParallel(
        left_df, right_df, left_on='words_left', right_on='words_right')
    # Set parameters
    fm_dask.set_parameter('how', 'inner')
    # Set parameters for multiprocessing
    fm_dask.set_parameter('parallel', True)
    fm_dask.set_parameter('dask_client', client)
    # Run the merge in dask
    result = fm_dask.merge()
    client.close()
    assert result.shape == (600, 2)
