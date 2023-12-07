"""

Functions to find matches between two lists of strings using dask.

Author: Oscar J. CASTRO-LOPEZ
Date: 2023-06-19

"""
from typing import Union, Callable
import dask.dataframe as dd
from dask.distributed import Client
from tqdm import tqdm
import pandas as pd
import numpy as np


def get_combinations_per_row(left_row: pd.Series,
                             right_np: np.ndarray,
                             left_on: str,
                             threshold: float,
                             ratio_function: Callable) -> Union[None, np.ndarray]:
    """Get matches between a row of left_df and all rows from right_df.

    Args:
        left_row (pd.Series): Row of left dataframe.
        right_np (np.ndarray): The right dataframe in numpy format with the index and string column.
        left_on (str): Name of the left column.
        threshold (float): Threshold for the ratio function.
        ratio_function (Callable): ratio function.

    Returns:
        None | np.ndarray: Matches found.
    """
    # Get ratios for each combination
    ratio_row = np.vectorize(ratio_function)(left_row[left_on], right_np[:, 1])
    # Get values that are larger or equal to threshold
    logic_idx = np.where(ratio_row >= threshold)[0]
    # Get the actual indices of the list_right
    right_idx = right_np[logic_idx, 0]
    # If there is no match return None
    if right_idx.shape[0] == 0:
        return None
    # Create meshgrid of indices
    grid_indices = np.meshgrid(left_row['index'], right_idx)
    # Stack the arrays column-wise
    combinations = np.column_stack(grid_indices)
    # Set type to int
    combinations = combinations.astype(int)
    return combinations


def get_combinations_per_partition(left_df: pd.DataFrame,
                                   right_np: np.ndarray,
                                   left_on: str,
                                   threshold: float,
                                   ratio_function: Callable) -> np.ndarray:
    """Function to process partitions of a dask dataframe. Calls apply to each row of left_df to obtain the matches.

    Args:
        left_df (pd.DataFrame): The left dataframe with the index and string column.
        right_np (np.ndarray): The right dataframe in numpy format with the index and string column.
        left_on (str): Name of the left column.
        threshold (float): Threshold for the ratio function.
        ratio_function (Callable): ratio function.

    Returns:
        np.ndarray: Matches found per partition.
    """
    results = left_df.apply(get_combinations_per_row, axis=1, args=(
        right_np, left_on, threshold, ratio_function))
    # Discard None values which means there is no match
    values = [value for value in results if value is not None]
    # If there is no match return empty array
    if len(values) == 0:
        return np.empty((0, 2))
    # Concatenate values
    merged_list = np.concatenate([sublist for sublist in values])
    return merged_list


def get_unique_nodes_count(dask_client: Client) -> int:
    """Get the number of uniques nodes in a dask client.

    Args:
        dask_client (Client): Dask client

    Returns:
        int: Number of nodes.
    """
    # Get the scheduler information
    scheduler_info = dask_client.scheduler_info()

    # Extract the set of unique hostnames from the workers
    unique_nodes = set(worker['host']
                       for worker in scheduler_info['workers'].values())

    # Get the number of different nodes
    num_nodes = len(unique_nodes)

    return num_nodes


def match_by_left_dask(left_tmp: pd.DataFrame,
                       right_np: np.ndarray,
                       left_on: str,
                       threshold: float,
                       dask_client: Client,
                       ratio_function: Callable,
                       hide_progress: bool = False) -> pd.DataFrame:
    """Parallel implementation of the function :func:`_match_by_left` with Dask.

    Args:
        left_tmp (pd.DataFrame): The left dataframe with the index and string column.
        right_np (np.ndarray): The right dataframe in numpy format with the index and string column.
        left_on (str): Name of the left column.
        threshold (float): Threshold for the ratio function.
        dask_client (Client) Dask client.
        ratio_function (Callable): ratio function.
        hide_progress(bool): Hide progress bar. Defaults to False.

    Returns:
        pd.DataFrame: A dataframe with two columns with the matched indices.
    """
    # Define the step size
    step_size = 100000
    # Get the chunk number based on step_size for the right data (numpy array)
    right_nchunks = int(np.ceil(right_np.shape[0] / step_size))
    # Split the right data (numpy array) into chunks
    right_chunks = np.array_split(right_np, right_nchunks)
    # Get number of nodes to calculate the number of partitions to use in dask
    num_nodes = get_unique_nodes_count(dask_client)
    # 1000 partitions for each node.
    n_parts = int(num_nodes * 1000)
    # Convert left dataframe to dask dataframe and load it in memory
    left_dd = dd.from_pandas(left_tmp, n_parts)
    left_dd = left_dd.persist()
    result = []
    n_matches = 0
    # Iterate over the chunks of the right data
    # Each iteration we scatter a right chunk of data, call map_partitions and append the result
    for right_chunk in tqdm(right_chunks, disable=hide_progress, desc=f"Matches {n_matches}"):
        res_tmp = left_dd.map_partitions(
            get_combinations_per_partition, right_chunk, left_on, threshold, ratio_function, align_dataframes=False)
        matched = res_tmp.compute()
        n_matches += matched.shape[0]
        result.append(matched)
    del left_dd
    # Stack the results
    matched_np = np.vstack(result)
    # Convert into a dataframe for future merge
    matched = pd.DataFrame(matched_np, columns=['leftind', 'rightind']).astype(
        {'leftind': 'Int64', 'rightind': 'Int64'})
    return matched
