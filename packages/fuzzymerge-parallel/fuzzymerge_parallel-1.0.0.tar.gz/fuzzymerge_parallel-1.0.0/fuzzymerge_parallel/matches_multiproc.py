"""

Functions to find matches between two lists of strings using multiprocessing.

Author: Oscar J. CASTRO-LOPEZ
Date: 2023-06-19

"""
from multiprocessing import shared_memory
from typing import Union, Callable
import multiprocessing as mp
from functools import partial
from tqdm import tqdm
import pandas as pd
import numpy as np


def _create_shared_array(right_np: np.ndarray):
    """Create a shared array to be used by all the threads.

    Args:
        right_np (np.ndarray): The array to put in shared memory

    Returns:
        SharedMemory: A shared memory descriptor
    """
    try:
        shm = shared_memory.SharedMemory(
            create=True, size=right_np.nbytes, name='left_aB3cD7eF9g')
    except FileExistsError:
        shm = shared_memory.SharedMemory(
            create=False, size=right_np.nbytes, name='left_aB3cD7eF9g')
    except Exception as shm_error:
        print('Error creating shared memory.', str(shm_error))
        return 0
    shared_right = np.ndarray(
        right_np.shape, dtype=right_np.dtype, buffer=shm.buf)
    shared_right[:] = right_np[:]
    return shm


def _get_matches_row_list(right_shape: tuple,
                          arr_type: Union[type, str],
                          threshold: float,
                          ratio_function: Callable,
                          left_row: np.ndarray) -> np.ndarray:
    """Get maches between one row with a string column and an array with a string column.

    Args:
        right_shape (tuple): Tuple with the shape of the right_np array.
        arr_type (Union[type, str]): The dtype of the right_np array.
        threshold (float): Threshold to apply to the ratio obtained.
        left_row (np.ndarray): One row of a numpy array of two columns.
        First column is an integer index. Second column is of strings (object).

    Returns:
        np.ndarray: A two column array with the matches obtained. Left column is left_np index and right column are right_np index.
    """
    # Load data from shared memory
    shm = shared_memory.SharedMemory(name='left_aB3cD7eF9g', create=False)
    right_np = np.ndarray(right_shape, dtype=arr_type, buffer=shm.buf)
    # Get row of ratios left row vs all right rows
    ratios = np.vectorize(ratio_function)(left_row[1], right_np[:, 1])

    # Get logical index where ratio >= Threshold
    log_idx = np.where(ratios >= threshold)[0]
    # Get the actual indices of the right rows
    right_idx = right_np[log_idx, 0]
    # Get combinations
    meshgrid = np.meshgrid(left_row[0], right_idx)
    # Stack in columns
    combinations = np.column_stack(meshgrid)
    # Convert to integer type
    return combinations.astype(int)


def match_by_left_multiproc(left_batches: list,
                            right_np: np.ndarray,
                            threshold: float,
                            n_threads: [int, str],
                            ratio_function: Callable,
                            hide_progress: bool = False) -> np.ndarray:
    """Parallel implementation of the function :func:`_match_by_left` with multiprocessing."""
    # Determine the number of threads to use if not a number or if lower than 1 is equal to available cores
    if n_threads == 'all' or (not isinstance(n_threads, int)) or (n_threads < 1):
        n_threads = mp.cpu_count()
    # Create shared memory data
    shm = _create_shared_array(right_np)
    matched_batch_list = []
    # Create a multiprocessing pool
    with mp.Pool(n_threads) as pool:
        n_matches = 0
        # Launch threads. Each thread gets matches between one row of left_np and right_np.
        singlefunc = partial(_get_matches_row_list,
                             right_np.shape, right_np.dtype, threshold, ratio_function)
        for left_batch in tqdm(left_batches, disable=hide_progress, desc=f"Matches {n_matches}"):
            # Apply the partial function to each row of left_np in parallel
            results = pool.map(singlefunc, left_batch)
            # Stack results into a single array
            matched = np.vstack(results)
            # Accumulate number of matches to print on progress bar
            n_matches += matched.shape[0]
            # Convert the matched array to a DataFrame
            matched_batch_df = pd.DataFrame(
                {'leftind': matched[:, 0], 'rightind': matched[:, 1]}, dtype=int)
            # Store partial results in a list
            matched_batch_list.append(matched_batch_df)
    # Concatenate all results
    matched_df = pd.concat(matched_batch_list)
    # Close and unlink shared memory
    shm.close()
    shm.unlink()
    return matched_df
