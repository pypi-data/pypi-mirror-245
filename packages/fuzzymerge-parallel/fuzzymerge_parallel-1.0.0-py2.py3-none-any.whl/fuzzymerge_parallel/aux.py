"""

Auxiliary functions for FuzzyMergeParallel.

Author: Oscar J. CASTRO-LOPEZ
Date: 2023-06-19

"""
import psutil
import pandas as pd


def _conditional_print(msg: str, enabled: bool = False):
    if enabled:
        print(msg)


def suggest_batch_number(df1: pd.DataFrame,
                         df2: pd.DataFrame,
                         scenario: int = 5,
                         factor: float = 0.001,
                         print_enabled: bool = False) -> int:
    """Compute how much memory would be required to execute FuzzyMergeParallel between two dataframes.

    Generates scenarios and returns how many rows per batch fit into memory to execute FuzzyMergeParallel.

    Args:
        df1 (pd.DataFrame): A pandas data frame.
        df2 (pd.DataFrame): A pandas data frame.
        scenario (int, optional): Scenario options from worst to best (1 to 8). Defaults to 5.
        factor (float, optional): Custom factor scenario. Defaults to 0.001.
        print_output (bool, optional): Prints the logic of the scenarios. Defaults to False.

    Returns:
        int: Number of rows to process per batch.
    """
    # Calculate the memory usage of each DataFrame in MB
    memory_usage_df1 = df1.memory_usage(deep=True).sum() / (1024 * 1024 * 1024)
    memory_usage_df2 = df2.memory_usage(deep=True).sum() / (1024 * 1024 * 1024)

    # Print the memory usage of each DataFrame
    _conditional_print(
        f"DataFrame 1 memory usage: {round(memory_usage_df1, 2)} GB - Rows: {df1.shape[0]}", print_enabled)
    _conditional_print(
        f"DataFrame 2 memory usage: {round(memory_usage_df2, 2)} GB - Rows: {df2.shape[0]}", print_enabled)

    # Calculate the memory required for the cross product
    # Worst case
    memory_required = (memory_usage_df1 *
                       df2.shape[0] + memory_usage_df2 * df1.shape[0])

    # Get the available system memory
    system_memory = psutil.virtual_memory().available / (1024 * 1024 * 1024)

    # Dictionary of scenarios
    scenarios = {
        1: {'msg': '1. Worst-case all rows match (Non-realistic)', 'mem_req': round(memory_required, 2)},
        2: {'msg': '2. Half rows match (Non-realistic)', 'mem_req':  round(memory_required * 0.5, 2)},
        3: {'msg': '3. Quarter rows match (25%)  (Unlikely)', 'mem_req':  round(memory_required * 0.25, 2)},
        4: {'msg': '4. Ten percent rows match (10%)', 'mem_req':  round(memory_required * 0.1, 2)},
        5: {'msg': '5. Five percent rows match (5%)', 'mem_req':  round(memory_required * 0.05, 2)},
        6: {'msg': '6. 2.5% rows match', 'mem_req':  round(memory_required * 0.025, 2)},
        7: {'msg': '7. 1% rows match', 'mem_req':  round(memory_required * 0.01, 2)},
        8: {'msg': '8. Custom factor', 'mem_req':  round(memory_required * factor, 2)},
    }

    for _, inner_dict in scenarios.items():
        _conditional_print(
            f"Memory required for {inner_dict['msg']}: {inner_dict['mem_req']} GB", print_enabled)

    # Compare the memory required with the available system memory
    if memory_required <= system_memory:
        _conditional_print(
            "Available system memory is sufficient.", print_enabled)
    else:
        _conditional_print(
            "Insufficient system memory for the cross product operation.", print_enabled)

    _conditional_print(
        f"You selected: {scenarios[scenario]['msg']}", print_enabled)
    memory_required = scenarios[scenario]['mem_req']

    overhead = 0.3
    available_memory = system_memory * (1 - overhead)
    _conditional_print(
        f"Avaliable memory - overhead: {round(available_memory, 2)}", print_enabled)
    batch_size = memory_required / available_memory
    batch_rows = df1.shape[0] / batch_size
    if batch_rows > df1.shape[0]:
        batch_rows = df1.shape[0]
    _conditional_print(
        f"Rows per batch: {round(batch_rows, 2)}", print_enabled)
    return int(batch_rows)
