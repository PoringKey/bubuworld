"""Standard statistical functions for funckey library."""

import math
from typing import List, Tuple, Union
from collections import Counter


def mean(data: List[Union[int, float]]) -> float:
    """Calculate the arithmetic mean (average) of a dataset.
    
    Args:
        data: List of numbers
        
    Returns:
        The mean value
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate mean of empty dataset")
    return sum(data) / len(data)


def median(data: List[Union[int, float]]) -> Union[int, float]:
    """Calculate the median of a dataset.
    
    Args:
        data: List of numbers
        
    Returns:
        The median value
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate median of empty dataset")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        middle1 = sorted_data[n // 2 - 1]
        middle2 = sorted_data[n // 2]
        return (middle1 + middle2) / 2


def mode(data: List[Union[int, float]]) -> Union[int, float]:
    """Calculate the mode (most frequent value) of a dataset.
    
    Args:
        data: List of numbers
        
    Returns:
        The mode value
        
    Raises:
        ValueError: If data is empty or has no unique mode
    """
    if not data:
        raise ValueError("Cannot calculate mode of empty dataset")
    
    counter = Counter(data)
    mode_value = counter.most_common(1)[0][0]
    return mode_value


def variance(data: List[Union[int, float]], sample: bool = False) -> float:
    """Calculate the variance of a dataset.
    
    Args:
        data: List of numbers
        sample: If True, calculate sample variance (divide by n-1). Default is False (population variance).
        
    Returns:
        The variance
        
    Raises:
        ValueError: If data is empty or has insufficient data for sample variance
    """
    if not data:
        raise ValueError("Cannot calculate variance of empty dataset")
    
    if sample and len(data) < 2:
        raise ValueError("Need at least 2 data points for sample variance")
    
    mean_value = mean(data)
    squared_diff_sum = sum((x - mean_value) ** 2 for x in data)
    divisor = len(data) - 1 if sample else len(data)
    
    return squared_diff_sum / divisor


def std_dev(data: List[Union[int, float]], sample: bool = False) -> float:
    """Calculate the standard deviation of a dataset.
    
    Args:
        data: List of numbers
        sample: If True, calculate sample standard deviation. Default is False (population).
        
    Returns:
        The standard deviation
        
    Raises:
        ValueError: If data is empty or has insufficient data for sample std dev
    """
    return math.sqrt(variance(data, sample=sample))


def min_value(data: List[Union[int, float]]) -> Union[int, float]:
    """Find the minimum value in a dataset.
    
    Args:
        data: List of numbers
        
    Returns:
        The minimum value
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot find minimum of empty dataset")
    return min(data)


def max_value(data: List[Union[int, float]]) -> Union[int, float]:
    """Find the maximum value in a dataset.
    
    Args:
        data: List of numbers
        
    Returns:
        The maximum value
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot find maximum of empty dataset")
    return max(data)


def range_value(data: List[Union[int, float]]) -> Union[int, float]:
    """Calculate the range (max - min) of a dataset.
    
    Args:
        data: List of numbers
        
    Returns:
        The range
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate range of empty dataset")
    return max_value(data) - min_value(data)


def quartiles(data: List[Union[int, float]]) -> Tuple[float, float, float]:
    """Calculate the quartiles (Q1, Q2, Q3) of a dataset.
    
    Args:
        data: List of numbers
        
    Returns:
        A tuple of (Q1, Q2, Q3) where Q2 is the median
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate quartiles of empty dataset")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    q2 = median(sorted_data)
    
    # Q1: median of lower half
    lower_half = sorted_data[:n // 2]
    q1 = median(lower_half)
    
    # Q3: median of upper half
    upper_half = sorted_data[(n + 1) // 2:]
    q3 = median(upper_half)
    
    return (q1, q2, q3)


def covariance(data1: List[Union[int, float]], data2: List[Union[int, float]], sample: bool = False) -> float:
    """Calculate the covariance between two datasets.
    
    Args:
        data1: First list of numbers
        data2: Second list of numbers
        sample: If True, calculate sample covariance. Default is False (population).
        
    Returns:
        The covariance
        
    Raises:
        ValueError: If datasets are empty or have different lengths
    """
    if not data1 or not data2:
        raise ValueError("Cannot calculate covariance with empty dataset")
    
    if len(data1) != len(data2):
        raise ValueError("Datasets must have the same length")
    
    if sample and len(data1) < 2:
        raise ValueError("Need at least 2 data points for sample covariance")
    
    mean1 = mean(data1)
    mean2 = mean(data2)
    
    product_sum = sum((x - mean1) * (y - mean2) for x, y in zip(data1, data2))
    divisor = len(data1) - 1 if sample else len(data1)
    
    return product_sum / divisor


def correlation(data1: List[Union[int, float]], data2: List[Union[int, float]]) -> float:
    """Calculate the Pearson correlation coefficient between two datasets.
    
    Args:
        data1: First list of numbers
        data2: Second list of numbers
        
    Returns:
        The correlation coefficient (between -1 and 1)
        
    Raises:
        ValueError: If datasets are empty, have different lengths, or have zero standard deviation
    """
    if not data1 or not data2:
        raise ValueError("Cannot calculate correlation with empty dataset")
    
    if len(data1) != len(data2):
        raise ValueError("Datasets must have the same length")
    
    std1 = std_dev(data1)
    std2 = std_dev(data2)
    
    if std1 == 0 or std2 == 0:
        raise ValueError("Cannot calculate correlation when standard deviation is zero")
    
    cov = covariance(data1, data2)
    return cov / (std1 * std2)
