"""Standard statistical functions for funckey library."""

import math
from typing import List, Tuple, Union, Dict
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


def ks_statistic(good_data: List[Union[int, float]], bad_data: List[Union[int, float]]) -> Dict[str, float]:
    """Calculate Kolmogorov-Smirnov (KS) statistic for credit scoring models.
    
    The KS statistic measures the maximum separation between cumulative distributions
    of good and bad customers. Higher KS values (closer to 1) indicate better model
    discrimination. Used extensively in credit risk modeling.
    
    Args:
        good_data: List of scores for good customers (non-defaulters)
        bad_data: List of scores for bad customers (defaulters)
        
    Returns:
        Dictionary containing:
            - 'ks_statistic': The maximum difference between cumulative distributions
            - 'good_cum_dist': Cumulative distribution of good customers
            - 'bad_cum_dist': Cumulative distribution of bad customers
            - 'max_diff_index': Index where maximum difference occurs
            
    Raises:
        ValueError: If either dataset is empty
        
    Example:
        >>> good = [0.7, 0.75, 0.8, 0.85, 0.9]
        >>> bad = [0.2, 0.3, 0.4, 0.45, 0.5]
        >>> result = ks_statistic(good, bad)
        >>> print(f"KS Statistic: {result['ks_statistic']:.4f}")
    """
    if not good_data or not bad_data:
        raise ValueError("Both good_data and bad_data must be non-empty")
    
    # Combine and sort all data
    all_data = sorted(set(good_data + bad_data))
    
    # Calculate cumulative distributions
    good_count = len(good_data)
    bad_count = len(bad_data)
    
    good_cum = []
    bad_cum = []
    
    for threshold in all_data:
        good_cum.append(sum(1 for x in good_data if x <= threshold) / good_count)
        bad_cum.append(sum(1 for x in bad_data if x <= threshold) / bad_count)
    
    # Calculate maximum difference
    differences = [abs(g - b) for g, b in zip(good_cum, bad_cum)]
    ks_value = max(differences)
    max_diff_index = differences.index(ks_value)
    
    return {
        'ks_statistic': ks_value,
        'good_cum_dist': good_cum,
        'bad_cum_dist': bad_cum,
        'max_diff_index': max_diff_index,
        'threshold_at_max': all_data[max_diff_index]
    }


def psi(expected_dist: Dict[str, float], actual_dist: Dict[str, float]) -> float:
    """Calculate Population Stability Index (PSI) for model monitoring.
    
    PSI measures the shift in distribution between two populations (e.g., training vs test
    data or baseline vs current period). Values:
    - PSI < 0.1: Negligible population change
    - 0.1 <= PSI < 0.25: Small population change
    - PSI >= 0.25: Significant population change (model retraining recommended)
    
    Args:
        expected_dist: Dictionary mapping bin/category to expected proportion
        actual_dist: Dictionary mapping bin/category to actual proportion
        
    Returns:
        The Population Stability Index (0 to infinity)
        
    Raises:
        ValueError: If distributions are empty or don't have matching keys
        
    Example:
        >>> expected = {'bin_1': 0.2, 'bin_2': 0.3, 'bin_3': 0.5}
        >>> actual = {'bin_1': 0.25, 'bin_2': 0.35, 'bin_3': 0.4}
        >>> psi_value = psi(expected, actual)
        >>> print(f"PSI: {psi_value:.4f}")
    """
    if not expected_dist or not actual_dist:
        raise ValueError("Both distributions must be non-empty")
    
    if set(expected_dist.keys()) != set(actual_dist.keys()):
        raise ValueError("Expected and actual distributions must have the same bins/categories")
    
    psi_value = 0.0
    
    for bin_name in expected_dist.keys():
        expected_prop = expected_dist[bin_name]
        actual_prop = actual_dist[bin_name]
        
        # Handle zero proportions with small epsilon
        epsilon = 1e-10
        expected_prop = max(expected_prop, epsilon)
        actual_prop = max(actual_prop, epsilon)
        
        # PSI formula: sum((actual% - expected%) * ln(actual%/expected%))
        psi_value += (actual_prop - expected_prop) * math.log(actual_prop / expected_prop)
    
    return psi_value


def psi_by_bins(expected_data: List[Union[int, float]], actual_data: List[Union[int, float]], 
                num_bins: int = 10) -> float:
    """Calculate PSI by automatically binning continuous data.
    
    This is a convenience function that bins continuous data into equal-width bins
    and then calculates PSI.
    
    Args:
        expected_data: List of expected/baseline values
        actual_data: List of actual/current values
        num_bins: Number of bins to create (default: 10)
        
    Returns:
        The Population Stability Index
        
    Raises:
        ValueError: If either dataset is empty or num_bins is invalid
        
    Example:
        >>> expected = [0.1, 0.2, 0.3, 0.4, 0.5]
        >>> actual = [0.15, 0.25, 0.35, 0.45, 0.55]
        >>> psi_value = psi_by_bins(expected, actual, num_bins=5)
        >>> print(f"PSI: {psi_value:.4f}")
    """
    if not expected_data or not actual_data:
        raise ValueError("Both datasets must be non-empty")
    
    if num_bins <= 0:
        raise ValueError("num_bins must be positive")
    
    # Get the range for binning
    all_data = expected_data + actual_data
    min_val = min(all_data)
    max_val = max(all_data)
    
    # Handle edge case where all values are the same
    if min_val == max_val:
        return 0.0
    
    # Create bins
    bin_edges = [min_val + (max_val - min_val) * i / num_bins for i in range(num_bins + 1)]
    
    # Assign data to bins
    def assign_to_bins(data: List[Union[int, float]]) -> Dict[str, float]:
        bin_counts = [0] * num_bins
        for value in data:
            for i in range(num_bins):
                if i == num_bins - 1:  # Last bin includes the max value
                    if bin_edges[i] <= value <= bin_edges[i + 1]:
                        bin_counts[i] += 1
                else:
                    if bin_edges[i] <= value < bin_edges[i + 1]:
                        bin_counts[i] += 1
                        break
        
        # Convert counts to proportions
        total = sum(bin_counts)
        return {f"bin_{i}": count / total for i, count in enumerate(bin_counts)}
    
    expected_dist = assign_to_bins(expected_data)
    actual_dist = assign_to_bins(actual_data)
    
    return psi(expected_dist, actual_dist)


def iv_statistic(good_data: List[Union[int, float]], bad_data: List[Union[int, float]], 
                 num_bins: int = 10) -> Dict[str, Union[float, Dict]]:
    """Calculate Information Value (IV) for feature selection in credit scoring.
    
    IV measures the strength of a variable's relationship with the target variable.
    Values:
    - IV < 0.02: Not useful
    - 0.02 <= IV < 0.1: Weak predictive power
    - 0.1 <= IV < 0.3: Medium predictive power
    - 0.3 <= IV < 0.5: Strong predictive power
    - IV >= 0.5: Excellent predictive power
    
    Args:
        good_data: List of feature values for good customers
        bad_data: List of feature values for bad customers
        num_bins: Number of bins to create (default: 10)
        
    Returns:
        Dictionary containing:
            - 'iv': The Information Value
            - 'bin_details': Details for each bin
            
    Raises:
        ValueError: If either dataset is empty
        
    Example:
        >>> good = [0.7, 0.75, 0.8, 0.85, 0.9, 0.92, 0.95]
        >>> bad = [0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6]
        >>> result = iv_statistic(good, bad)
        >>> print(f"Information Value: {result['iv']:.4f}")
    """
    if not good_data or not bad_data:
        raise ValueError("Both good_data and bad_data must be non-empty")
    
    if num_bins <= 0:
        raise ValueError("num_bins must be positive")
    
    # Get the range for binning
    all_data = good_data + bad_data
    min_val = min(all_data)
    max_val = max(all_data)
    
    if min_val == max_val:
        return {'iv': 0.0, 'bin_details': {}}
    
    # Create bins
    bin_edges = [min_val + (max_val - min_val) * i / num_bins for i in range(num_bins + 1)]
    
    # Count good and bad in each bin
    bin_details = {}
    total_good = len(good_data)
    total_bad = len(bad_data)
    iv_value = 0.0
    epsilon = 1e-10
    
    for i in range(num_bins):
        # Count good and bad in this bin
        if i == num_bins - 1:  # Last bin includes the max value
            good_count = sum(1 for x in good_data if bin_edges[i] <= x <= bin_edges[i + 1])
            bad_count = sum(1 for x in bad_data if bin_edges[i] <= x <= bin_edges[i + 1])
        else:
            good_count = sum(1 for x in good_data if bin_edges[i] <= x < bin_edges[i + 1])
            bad_count = sum(1 for x in bad_data if bin_edges[i] <= x < bin_edges[i + 1])
        
        # Calculate distributions
        good_pct = good_count / total_good if total_good > 0 else 0
        bad_pct = bad_count / total_bad if total_bad > 0 else 0
        
        # Handle zero percentages
        good_pct = max(good_pct, epsilon)
        bad_pct = max(bad_pct, epsilon)
        
        # IV for this bin: (bad% - good%) * ln(bad%/good%)
        bin_iv = (bad_pct - good_pct) * math.log(bad_pct / good_pct)
        iv_value += bin_iv
        
        bin_details[f"bin_{i}"] = {
            'range': (bin_edges[i], bin_edges[i + 1]),
            'good_count': good_count,
            'bad_count': bad_count,
            'good_pct': good_pct,
            'bad_pct': bad_pct,
            'iv': bin_iv
        }
    
    return {
        'iv': iv_value,
        'bin_details': bin_details
    }
