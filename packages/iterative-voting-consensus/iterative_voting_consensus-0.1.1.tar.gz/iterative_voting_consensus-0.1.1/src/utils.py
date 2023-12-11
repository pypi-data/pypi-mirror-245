import numpy as np


def random_initialization(n_value: int, max_value: int) -> np.ndarray:
    """Random initialization of the pi_star partition.

    Parameters
    ----------
    n_value : int
        Number of data points
    max_value : int
        Maximal number of clusters

    Returns
    -------
    np.ndarray of shape (n_value)
        Random partition
    """
    return np.random.randint(low=0, high=max_value, size=n_value)
