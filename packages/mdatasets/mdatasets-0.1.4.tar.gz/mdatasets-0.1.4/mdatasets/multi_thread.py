import os
import multiprocessing

def cpu_info():
    """
    Retrieve information about the CPU.

    Returns:
    - cpu_count (int): The number of physical CPU cores.
    - logical_cores (int): The total number of logical CPU cores (including hyper-threading).

    Example:
    >>> cpu_count, logical_cores = get_cpu_info()
    >>> print(f"Physical CPU cores: {cpu_count}, Logical CPU cores: {logical_cores}")
    Physical CPU cores: 4, Logical CPU cores: 8
    """

    cpu_count = os.cpu_count()
    logical_cores = multiprocessing.cpu_count()
    return cpu_count, logical_cores
