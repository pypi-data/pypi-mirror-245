"""

FuzzyMergeParallel.

Package for performing fuzzy merging of two dataframes based on a string column, using a distance function such as Levenshtein.

FuzzyMergeParallel offers two modes for faster execution:

1. Multiprocessing mode: This mode runs on a single machine using multiple CPU cores. It's ideal for local processing tasks, utilizing Numpy and Python's multiprocessing libraries to speed things up.
2. Dask mode: In this mode, FuzzyMergeparallel utilizes a Dask client, which can be configured for single or multi-node setups. Multi-node clients distribute computations across clusters of machines, making it suitable for heavy-duty processing.


Author: Oscar J. CASTRO-LOPEZ
Date: 2023-06-19

Classes:
    FuzzyMergeParallel:
        A class for configuring and executing parallel fuzzy merging.

Functions:
    FuzzyMergeParallel.merge(args):
        Executes the fuzzy merge operation.

Notes:
    The code can also run on a single procesor.
    This class is based on the Levenpandas package: https://github.com/fangzhou-xie/levenpandas
"""
from typing import Any
import numpy as np
import pandas as pd
from fuzzymerge_parallel.aux import suggest_batch_number

from fuzzymerge_parallel.matches_multiproc import match_by_left_multiproc
from Levenshtein import ratio as levenshtein_ratio
from tqdm import tqdm


class FuzzyMergeParallel:
    """A class for performing fuzzy merges between two Pandas data frames.

    The merge can be executed sequentially, in parallel using multiprocessing (single-node), or in parallel using Dask (multi-node).

    Usage:
    1. Initialize an instance of the FuzzyMergeParallel class with the input Pandas data frames and the columns to merge.
    2. Configure the matching criteria, threshold values, computing options, and other parameters for the merge operation.
    3. Invoke the merge method to perform the fuzzy merge between the data frames.
    4. Access the merged data frame or retrieve summary statistics about the matches.

    If using Dask, a Dask client object must be provided.

    Examples:
    ```
    fuzzy_merger = FuzzyMergeParallel(left_df, right_df, left_on='left_column_name', right_on='right_column_name')
    # Set parameters
    fuzzy_merger.set_parameter('how', 'inner')
    fuzzy_merger.set_parameter('parallel', False)
    # Run the merge sequentially
    result = fuzzy_merger.merge()

    # Set parameters for multiprocessing
    
    fuzzy_merger.set_parameter('n_threads', 64)
    # Run the merge multiprocessing
    result = fuzzy_merger.merge()
    # Set parameters for dask
    ## Create a dask client
    from dask.distributed import Client
    client = Client(...)  # Connect to distributed cluster and override default
    fuzzy_merger.set_parameter('parallel', True)
    fuzzy_merger.set_parameter('dask_client', client)
    # Run the merge in dask
    result = fuzzy_merger.merge()
    ```
    """

    def __init__(self, left, right, left_on=None, right_on=None):
        """
        Initialize a FuzzyMergeParallel object.

        Parameters:
            left: DataFrame
                The left input data to be merged.
            right: DataFrame
                The right input data to be merged.
            left_on: str, optional
                Column(s) in the left DataFrame to use as merge keys.
            right_on: str, optional
                Column(s) in the right DataFrame to use as merge keys.


        Other Attributes:
            uselower: bool
                Whether to convert strings to lowercase before comparison. Default is True.
            threshold: float
                The threshold value for fuzzy matching similarity. Default is 0.9.
            how: str, optional
                The type of merge to be performed. Default is 'outer'.
            on: str or None
                Column(s) to merge on if not specified in left_on or right_on.
            left_index: bool
                Whether to use the left DataFrame's index as merge key(s). Default is False.
            right_index: bool
                Whether to use the right DataFrame's index as merge key(s). Default is False.
            parallel: bool
                Whether to perform the merge operation in parallel. Default is True.
            n_threads: int
                The number of threads to use for parallel execution. Default is 'all' which runs one thread per available core.
            hide_progress: bool
                Whether to display a progress bar during the merge operation. Default is False.
            num_batches: int
                The number of batches to split the ratio computation. Default is automatic.
            ratio_function: runnable
                The distance ratio function. Defaults to `Levenshtein.ratio()`.
            dask_client: client
                A dask client object.
        """
        self.left = left
        self.right = right
        self.left_on = left_on
        self.right_on = right_on
        # Other attributes by default
        self.uselower = True
        self.threshold = 0.9
        self.how = 'outer'
        self.on = None
        self.left_index = False
        self.right_index = False
        self.parallel = True
        self.n_threads = 'all'
        self.hide_progress = False
        self.ratio_function = levenshtein_ratio
        self.dask_client = None

        # Get number of batches automatically
        # Define the batch size in number of rows
        batch_size = suggest_batch_number(
            self.left, self.right, print_enabled=False)
        # Get the total number of rows in the DataFrame
        total_rows = len(self.left)
        # Calculate the number of batches needed
        self.num_batches = (total_rows + batch_size - 1) // batch_size

    def set_parameter(self, parameter: str, value: Any):
        """Set a parameter to the `FuzzyMergeParallel` class.

        Args:
            parameter (str): Name of the parameter.
            value (any): Value to assign to the parameter
        """
        setattr(self, parameter, value)

    def __repr__(self):
        """Print a summary of the FuzzyMergeParallel object."""
        attributes = vars(self)
        attribute_strings = []

        for key, value in attributes.items():
            if isinstance(value, pd.DataFrame):
                attribute_strings.append(
                    f"{key} = {value.shape} - {value.columns}")
            else:
                attribute_strings.append(f"{key} = {value}")

        return "\n".join(attribute_strings)

    def merge(self):
        """Run the Fuzzy merge process and returns a data frame with merged dataframe with the matches.

        Returns:
            pd.DataFrame: A pandas dataframe with the merge result.
        """
        # Variables setting and validation
        if self.left_index:
            self.left_on = self.left_index

        if self.right_index:
            self.right_on = self.right_index

        if self.on:
            self.left_on = self.on
            self.right_on = self.on

        merge_on, delete_on = 'leftind', 'rightind'
        if self.how in ('left', 'inner'):
            merge_on, delete_on = 'leftind', 'rightind'
        elif self.how in ('right', 'outer'):
            merge_on, delete_on = 'rightind', 'leftind'
        else:
            raise ValueError(
                f"Parameter how not valid: {self.how}. Must be: left, inner, right, or outer.")

        if self.left_on is not None and self.left_on not in self.left.columns:
            raise KeyError(
                f"Column '{self.left_on}' does not exist in the left DataFrame")

        if self.right_on is not None and self.right_on not in self.right.columns:
            raise KeyError(
                f"Column '{self.right_on}' does not exist in the right DataFrame")

        left_tmp, right_tmp = self._get_np_subset()

        matched = self._match_by_left(left_tmp, right_tmp)

        mergeleft = self.left.merge(
            matched, how=self.how, left_index=True, right_on='leftind')

        mergeright = matched.merge(
            self.right, how=self.how, left_on='rightind', right_index=True)

        # Merge with simplified code
        merged = mergeleft.drop(columns=[delete_on]).merge(
            mergeright, how=self.how, on=merge_on).drop_duplicates(
            subset=[self.left_on, self.right_on]).drop(columns=['leftind', 'rightind'])

        if self.how in ['left', 'right', 'inner']:
            merged = merged.dropna(subset=[self.left_on] if self.how == 'left' else [self.right_on])
        elif self.how == 'outer':
            merged = merged.dropna(subset=[self.left_on, self.right_on], how='all')

        merged = merged.reset_index(drop=True)
        return merged

    def _get_np_subset(self):
        """Process the input dataframes to transform them into Numpy arrays with two columns.

            The first column is the index, the second column is the column of interest which is a string.

        Returns:
            Two numpy arrays
        """
        self.left = self.left.reset_index(drop=True)
        self.right = self.right.reset_index(drop=True)
        left_tmp = self.left.reset_index()[['index', self.left_on]].dropna(
            subset=[self.left_on])
        right_tmp = self.right.reset_index(
        )[['index', self.right_on]].dropna(subset=[self.right_on])

        if self.uselower:
            left_tmp[self.left_on] = left_tmp[self.left_on].str.lower()
            right_tmp[self.right_on] = right_tmp[self.right_on].str.lower()

        return left_tmp, right_tmp

    def _match_by_left(self, left_tmp: pd.DataFrame, right_tmp: pd.DataFrame) -> pd.DataFrame:
        """Apply a distance function between two dataframes that have a column of strings and returns a dataframe with the indices where the strings matched.

            Performs the following for each pair of strings of the two dataframes:
            1. Gets ratio between each pair of strings.
            2. Filters matches by the threshold.
            3. Returns a dataframe with the indices where the strings match according to the threshold.

            This function can run sequentially or in parallel by using multiprocessing.

        Args:
            left_tmp (pd.DataFrame): Dataframeof two columns. First column is an integer index. Second column is of strings (object).
            right_tmp (pd.DataFrame): Dataframeof two columns. First column is an integer index. Second column is of strings (object).

        Returns:
            pd.DataFrame: A two column dataframe containing the indices of the strings that match.
            First column are indices of left data, second column are indices of right data.
        """
        # Convert right dataframe to Numpy
        right_np = right_tmp[['index', self.right_on]].to_numpy()

        if self.parallel and self.dask_client is not None:  # Dask
            try:
                from fuzzymerge_parallel.matches_dask import match_by_left_dask
            except ImportError:
                import warnings
                warnings.warn(
                    "Dask dependencies not found, Please install 'fuzzymerge_parallel[dask]' to use this command.")
            else:
                matched = match_by_left_dask(left_tmp, right_np, self.left_on, self.threshold, self.dask_client, self.ratio_function, self.hide_progress)
                return matched

        # Convert left dataframe to Numpy
        left_np = left_tmp[['index', self.left_on]].to_numpy()

        print('Total batches:', self.num_batches,
              '| Rows per batch (approx):', left_np.shape[0] // self.num_batches)

        left_batches = np.array_split(left_np, self.num_batches)

        if self.parallel:  # multiprocessing
            matched = match_by_left_multiproc(left_batches, right_np, self.threshold, self.n_threads, self.ratio_function, self.hide_progress)
        else:  # Sequential
            matched = self._match_by_left_sequential(left_batches, right_np)
        return matched

    def _get_ratio_matrix(self, left_np: np.ndarray, right_np: np.ndarray) -> np.ndarray:
        """Apply a function to get the distance between two strings of each pair of two arrays.

        Args:
            left_np (np.ndarray): A one column array of strings.
            right_np (np.ndarray): A one column array of strings.

        Returns:
            np.ndarray: A Matrix with the difference measure between each pair of strings.
        """
        # Get rows and cols of matrix, create empty matrix to store results
        num_rows = left_np.shape[0]
        num_cols = right_np.shape[0]
        ratio_matrix = np.empty((num_rows, num_cols))
        for i in range(num_rows):
            ratio_matrix[i] = np.vectorize(
                self.ratio_function)(left_np[i], right_np)
        return ratio_matrix

    def _match_by_left_sequential(self,
                                  left_batches: list,
                                  right_np: np.ndarray) -> pd.DataFrame:
        """Sequential implementation of the function :func:`_match_by_left`."""
        # Iterate over each row pair and get Levenshtein ratio
        # for left_row in left_np:
        #    get_matches_left_row_mp(right_np, threshold, left_row)
        matched_batch_list = []
        n_matches = 0
        for left_batch in tqdm(left_batches, disable=self.hide_progress, desc=f"Matches {n_matches}"):
            # Get ratio matrix betwee left batch and right array
            ratio_matrix = self._get_ratio_matrix(
                left_batch[:, 1], right_np[:, 1])
            # Obtain the indexes where the ratio is >= than the threshold
            left_indices, right_indices = np.where(
                ratio_matrix >= self.threshold)
            # Get correct indices and convert to dataframe
            matched_batch = pd.DataFrame(
                {'leftind': left_batch[left_indices, 0], 'rightind': right_np[right_indices, 0]}, dtype=int)
            # Accumulate number of matches to print on progress bar
            n_matches += matched_batch.shape[0]
            matched_batch_list.append(matched_batch)

        matched = pd.concat(matched_batch_list)

        return matched
