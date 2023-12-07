# fuzzymerge_parallel

[![Python package](https://github.com/ULHPC/fuzzymerge_parallel/actions/workflows/python-package.yml/badge.svg)](https://github.com/ULHPC/fuzzymerge_parallel/actions/workflows/python-package.yml)

Merge two pandas dataframes by using a function to calculate the edit distance (Levenshtein Distance) using multiprocessing for parallelization on a single node or Dask for distributed computation across multiple nodes.

**Efficient Matching and Merging**

Matching and merging data can be demanding in terms of time and memory usage. That's why our package is specifically crafted to address these challenges effectively.

**Optimized Execution**

To boost execution performance, we've fine-tuned our package to work seamlessly in both single-node and multi-node environments. Whether you're processing data on a local machine or distributing tasks across a cluster, our package is optimized to get the job done efficiently.

**Smart Memory Management**

Memory efficiency is a priority. Our algorithm estimates memory requirements and divides the workload into manageable batches. This ensures that your data operations fit comfortably within your available memory. Plus, you have the flexibility to customize these settings to match your specific needs.

With this package, you can confidently tackle data matching and merging tasks while optimizing both time and memory resources.

## Description

fuzzymerge_parallel offers two modes for faster execution:

### 1. Multiprocessing mode

This mode runs on a single machine and it is able to use multi-CPU cores. This mode does not require dask and it's ideal for local processing tasks, utilizing Numpy and Python's multiprocessing libraries to speed things up.

### 2. Dask mode

In this mode, fuzzymerge_parallel utilizes a Dask client, which can be configured for single or multi-node setups. To leverage the dask mode it is suggested to use it with multiple nodes. Multi-node dask clients distribute computations across clusters of machines, making it suitable for heavy-duty processing. Using dask mode offers numerous benefits, automating tasks that would otherwise require manual intervention, such as enhancing performance, expanding scalability, ensuring fault tolerance, optimizing resource utilization, and enabling parallelism.

<span style="color:red">**Important remarks:**</span> When using the package on a single node, it is recommended to opt for the multiprocessing mode. This choice is driven by the fact that multiprocessing generally offers faster execution times compared to Dask on a single node. Dask introduces certain overheads, including data copying, fault tolerance mechanisms, and resource management, which may not be as beneficial in single-node scenarios. Therefore, it is strongly advisable to leverage Dask when deploying the package in a multi-node cluster.

 
### Features

- Performs fuzzy merging of dataframes based on string columns
- Utilize distance functions (e.g., Levenshtein) for intelligent matching
- Benefit from parallel computing techniques for enhanced performance
- Easily integrate into your existing data processing pipelines

## Installation

### Install from PyPi
To download and install the fuzzymerge_parallel Python package from PyPi, run the following instruction:

### Install from GitHub
To download and install the fuzzymerge_parallel Python package from GitHub, you can follow these improved instructions:
```bash
    pip install fuzzymerge-parallel
```

To install FuzzyMergeParallel via pip from its GitHub repository, follow these steps:

1. **Download the Package:** Begin by downloading the package from GitHub. You can use git to clone the repository to your local machine:
    ```bash
    git clone https://github.com/ULHPC/fuzzymerge_parallel.git
    ```
    
2. **Navigate to the Package Directory:** Open a terminal or command prompt and change your current directory to the downloaded package folder:
    ```bash
    cd fuzzymerge_parallel
    ```

3. **Install the Package:** Finally, use pip to install the package in "editable" mode (with the -e flag) to allow for development and updates. There are two options:

    **Option 1:** If you plan to use the package on a single node and don't need the dask and distributed dependencies, simply run:
    ```bash
    pip install -e .
    ```

    **Option 2:** If you intend to use the package in both single and multi-node environments with dask and distributed support, use the following command:
    ```bash
    pip install -e ".[dask]"
    ```


This command will install the package along with its dependencies. You can now import and use FuzzyMergeParallel in your Python projects.    

## Dependencies

To use this package, you will need to have the following dependencies installed:

- [Click](https://pypi.org/project/Click/) >= 7.0
- [dask[distributed]](https://pypi.org/project/dask/) >= 2023.5.0 (Optional: Only needed for multi-node)
- [Levenshtein](https://pypi.org/project/python-Levenshtein/) >= 0.21.0 (Optional: Only needed for multi-node)
- [nltk](https://pypi.org/project/nltk/) >= 3.8.1
- [numpy](https://pypi.org/project/numpy/) >= 1.23.5
- [pandas](https://pypi.org/project/pandas/) >= 1.5.3
- [tqdm](https://pypi.org/project/tqdm/) >= 4.65.0
- [psutil](https://pypi.org/project/psutil/) == 5.9.5
- [pytest](https://pypi.org/project/pytest/) >= 7.4.1

## Description

The FuzzyMergeParallel class is exposed and it is highly configurable. The following parameters and other attributes can be set up before doing the merge operation:



| Parameter        | Description                                                      |
|------------------|------------------------------------------------------------------|
| left             | The left input data to be merged.                                |
| right            | The right input data to be merged.                               |
| left_on          | Column(s) in the left DataFrame to use as merge keys.            |
| right_on         | Column(s) in the right DataFrame to use as merge keys.           |

Example create a FuzzyMergeParallel class:

```python
fuzzy_merger = FuzzyMergeParallel(left_df, right_df, left_on='left_column_name', right_on='right_column_name')
```


| Attribute        | Description                                                      |
|------------------|------------------------------------------------------------------|
| uselower         | Whether to convert strings to lowercase before comparison. Default is True.        |
| threshold        | The threshold value for fuzzy matching similarity. Default is 0.9.                |
| how              | The type of merge to be performed. Default is 'outer'.                               |
| on               | Column(s) to merge on if not specified in left_on or right_on. Default is False.    |
| left_index       | Whether to use the left DataFrame's index as merge key(s). Default is False.       |
| right_index      | Whether to use the right DataFrame's index as merge key(s). Default is False.      |
| parallel         | Whether to perform the merge operation in parallel. Default is True.              |
| n_threads        | The number of threads to use for parallel execution. Default is 'all' (a thread per each available core).             |
| hide_progress    | Whether to display a progress bar during the merge operation. Default is False.    |
| num_batches      | The number of batches to split the ratio computation. Default is automatic.              |
| ratio_function   | The distance ratio function.                Defaults to `Levenshtein.ratio()`.                      |
| dask_client      | A dask client object.                                            |

Example set extra attributes by stating the name of the attribute and its value with `set_parameter()`:

```python
fuzzy_merger.set_parameter('how', 'inner')
fuzzy_merger.set_parameter('threshold', 0.75)
```

## Usage


### Single node 

#### Sequential execution

```python
fuzzy_merger = FuzzyMergeParallel(left_df, right_df, left_on='left_column_name', right_on='right_column_name')
# Set parameters
fuzzy_merger.set_parameter('how', 'inner')
fuzzy_merger.set_parameter('parallel', False)
# Run the merge sequentially
result = fuzzy_merger.merge()
```

#### Multiprocessing execution

```python
fuzzy_merger = FuzzyMergeParallel(left_df, right_df, left_on='left_column_name', right_on='right_column_name')
# Set parameters
fuzzy_merger.set_parameter('how', 'inner')
fuzzy_merger.set_parameter('n_threads', 64)
# Run the merge multiprocessing
result = fuzzy_merger.merge()
```

### Multi-node (dask)

#### Local client

```python
fuzzy_merger = FuzzyMergeParallel(left_df, right_df, left_on='left_column_name', right_on='right_column_name')
# Set parameters
fuzzy_merger.set_parameter('how', 'inner')

# Set parameters for dask
## Create a dask client
from dask.distributed import Client
client = Client(...)  # Connect to distributed cluster and override default
fuzzy_merger.set_parameter('parallel', True)
fuzzy_merger.set_parameter('dask_client', client)
# Run the merge in dask
result = fuzzy_merger.merge()
```

How to create a dask client?

There are different options to create a dask client. Extensive documentation can be found on their websites:

- [General dask documentation](https://docs.dask.org/en/stable/)
- [dask client documentation](https://distributed.dask.org/en/stable/client.html)
- [Dask jobqueue documentation (distributed)](https://jobqueue.dask.org/en/latest/index.html)

A couple of examples:

```python
# Launch dask on a local cluster (singlenode)
from dask.distributed import Client, LocalCluster
# Create a local Dask cluster
cluster = LocalCluster()
# Create a Dask client to connect to the cluster
client = Client(cluster)
```

```python
# Launch dask on a SLURM cluster
from dask_jobqueue import SLURMCluster

cluster = SLURMCluster(
    queue='regular',
    account="myaccount",
    cores=128,
    memory="500 GB"
)

cluster.scale(jobs=10)  # ask for 10 jobs

client = Client(cluster)
```

## Contributing

Contributions are welcome! If you encounter any issues, have suggestions, or want to contribute improvements, please submit a pull request or open an issue on the GitHub repository.


## Authors

- Oscar J. Castro Lopez (oscar.castro@uni.lu)
  - Parallel Computing & Optimisation Group (PCOG) - **University of Luxembourg**


This package is based on the levenpandas package (https://github.com/fangzhou-xie/levenpandas).

## License

This project is licensed under the MIT License.