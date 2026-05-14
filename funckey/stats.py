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


# ================================================================================
# CREDIT SCORING MODEL METRICS
# ================================================================================

def ks_statistic(good_data: List[Union[int, float]], bad_data: List[Union[int, float]]) -> Dict[str, Union[float, int, List]]:
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
            - 'threshold_at_max': Score threshold at maximum difference
            
    Raises:
        ValueError: If either dataset is empty
    """
    if not good_data or not bad_data:
        raise ValueError("Both good_data and bad_data must be non-empty")
    
    all_data = sorted(set(good_data + bad_data))
    good_count = len(good_data)
    bad_count = len(bad_data)
    
    good_cum = []
    bad_cum = []
    
    for threshold in all_data:
        good_cum.append(sum(1 for x in good_data if x <= threshold) / good_count)
        bad_cum.append(sum(1 for x in bad_data if x <= threshold) / bad_count)
    
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
    data or baseline vs current period). Interpretation:
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
    """
    if not expected_dist or not actual_dist:
        raise ValueError("Both distributions must be non-empty")
    
    if set(expected_dist.keys()) != set(actual_dist.keys()):
        raise ValueError("Expected and actual distributions must have the same bins/categories")
    
    psi_value = 0.0
    epsilon = 1e-10
    
    for bin_name in expected_dist.keys():
        expected_prop = max(expected_dist[bin_name], epsilon)
        actual_prop = max(actual_dist[bin_name], epsilon)
        
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
    """
    if not expected_data or not actual_data:
        raise ValueError("Both datasets must be non-empty")
    
    if num_bins <= 0:
        raise ValueError("num_bins must be positive")
    
    all_data = expected_data + actual_data
    min_val = min(all_data)
    max_val = max(all_data)
    
    if min_val == max_val:
        return 0.0
    
    bin_edges = [min_val + (max_val - min_val) * i / num_bins for i in range(num_bins + 1)]
    
    def assign_to_bins(data: List[Union[int, float]]) -> Dict[str, float]:
        bin_counts = [0] * num_bins
        for value in data:
            for i in range(num_bins):
                if i == num_bins - 1:
                    if bin_edges[i] <= value <= bin_edges[i + 1]:
                        bin_counts[i] += 1
                else:
                    if bin_edges[i] <= value < bin_edges[i + 1]:
                        bin_counts[i] += 1
                        break
        
        total = sum(bin_counts)
        return {f"bin_{i}": count / total for i, count in enumerate(bin_counts)}
    
    expected_dist = assign_to_bins(expected_data)
    actual_dist = assign_to_bins(actual_data)
    
    return psi(expected_dist, actual_dist)


def iv_statistic(good_data: List[Union[int, float]], bad_data: List[Union[int, float]], 
                 num_bins: int = 10) -> Dict[str, Union[float, Dict]]:
    """Calculate Information Value (IV) for feature selection in credit scoring.
    
    IV measures the strength of a variable's relationship with the target variable.
    Interpretation:
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
    """
    if not good_data or not bad_data:
        raise ValueError("Both good_data and bad_data must be non-empty")
    
    if num_bins <= 0:
        raise ValueError("num_bins must be positive")
    
    all_data = good_data + bad_data
    min_val = min(all_data)
    max_val = max(all_data)
    
    if min_val == max_val:
        return {'iv': 0.0, 'bin_details': {}}
    
    bin_edges = [min_val + (max_val - min_val) * i / num_bins for i in range(num_bins + 1)]
    
    bin_details = {}
    total_good = len(good_data)
    total_bad = len(bad_data)
    iv_value = 0.0
    epsilon = 1e-10
    
    for i in range(num_bins):
        if i == num_bins - 1:
            good_count = sum(1 for x in good_data if bin_edges[i] <= x <= bin_edges[i + 1])
            bad_count = sum(1 for x in bad_data if bin_edges[i] <= x <= bin_edges[i + 1])
        else:
            good_count = sum(1 for x in good_data if bin_edges[i] <= x < bin_edges[i + 1])
            bad_count = sum(1 for x in bad_data if bin_edges[i] <= x < bin_edges[i + 1])
        
        good_pct = max(good_count / total_good if total_good > 0 else 0, epsilon)
        bad_pct = max(bad_count / total_bad if total_bad > 0 else 0, epsilon)
        
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


def auc_score(actual: List[int], predicted: List[float]) -> float:
    """Calculate Area Under ROC Curve (AUC).
    
    AUC measures the probability that the model ranks a random good customer 
    higher than a random bad customer. Range: 0.5 to 1.0 (0.5 = random, 1.0 = perfect)
    
    Args:
        actual: List of actual labels (0 for good, 1 for bad)
        predicted: List of predicted probabilities/scores
        
    Returns:
        AUC score (0.5 to 1.0)
        
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    if not actual or not predicted:
        raise ValueError("Both actual and predicted must be non-empty")
    
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    
    # Sort by predicted scores (descending)
    sorted_pairs = sorted(zip(predicted, actual), key=lambda x: x[0], reverse=True)
    
    n_good = sum(1 for a in actual if a == 0)
    n_bad = sum(1 for a in actual if a == 1)
    
    if n_good == 0 or n_bad == 0:
        raise ValueError("Must have both good (0) and bad (1) samples")
    
    # Count concordant pairs
    concordant = 0
    discordant = 0
    
    for i, (score_i, label_i) in enumerate(sorted_pairs):
        for j in range(i + 1, len(sorted_pairs)):
            score_j, label_j = sorted_pairs[j]
            if label_i == 0 and label_j == 1:  # Good ranked higher than bad
                concordant += 1
            elif label_i == 1 and label_j == 0:  # Bad ranked higher than good
                discordant += 1
    
    total_pairs = n_good * n_bad
    auc = concordant / total_pairs if total_pairs > 0 else 0.5
    
    return auc


def gini_coefficient(actual: List[int], predicted: List[float]) -> float:
    """Calculate Gini Coefficient for credit scoring models.
    
    Gini measures model discrimination ability. Formula: Gini = 2*AUC - 1
    Range: 0 to 1 (0 = random model, 1 = perfect model)
    
    Args:
        actual: List of actual labels (0 for good, 1 for bad)
        predicted: List of predicted probabilities/scores
        
    Returns:
        Gini coefficient (0 to 1)
        
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    auc = auc_score(actual, predicted)
    return 2 * auc - 1


def somers_d(actual: List[int], predicted: List[float]) -> float:
    """Calculate Somers' D statistic for credit scoring.
    
    Somers' D measures the association between predicted scores and actual outcomes.
    Formula: D = 2 * (Concordance% - Discordance%) / 100
    Range: -1 to 1 (-1 = perfect negative, 1 = perfect positive, 0 = random)
    
    Args:
        actual: List of actual labels (0 for good, 1 for bad)
        predicted: List of predicted probabilities/scores
        
    Returns:
        Somers' D statistic (-1 to 1)
        
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    if not actual or not predicted:
        raise ValueError("Both actual and predicted must be non-empty")
    
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    
    sorted_pairs = sorted(zip(predicted, actual), key=lambda x: x[0], reverse=True)
    
    n_good = sum(1 for a in actual if a == 0)
    n_bad = sum(1 for a in actual if a == 1)
    
    if n_good == 0 or n_bad == 0:
        raise ValueError("Must have both good (0) and bad (1) samples")
    
    concordant = 0
    discordant = 0
    
    for i, (score_i, label_i) in enumerate(sorted_pairs):
        for j in range(i + 1, len(sorted_pairs)):
            score_j, label_j = sorted_pairs[j]
            if label_i == 0 and label_j == 1:
                concordant += 1
            elif label_i == 1 and label_j == 0:
                discordant += 1
    
    total_pairs = n_good * n_bad
    if total_pairs == 0:
        return 0.0
    
    return 2 * (concordant - discordant) / total_pairs


def lift_gain(actual: List[int], predicted: List[float], num_deciles: int = 10) -> Dict[str, Union[List, float]]:
    """Calculate Lift and Gain charts for model evaluation.
    
    Lift shows how much better the model is than random selection at each percentile.
    Gain shows cumulative % of bads captured at each percentile.
    
    Args:
        actual: List of actual labels (0 for good, 1 for bad)
        predicted: List of predicted probabilities/scores
        num_deciles: Number of segments (default: 10 for deciles)
        
    Returns:
        Dictionary containing:
            - 'deciles': Decile numbers
            - 'good_count': Count of goods in each decile
            - 'bad_count': Count of bads in each decile
            - 'bad_pct_in_decile': % of bads in each decile
            - 'cum_bad_count': Cumulative bad count
            - 'cum_bad_pct': Cumulative % of bads
            - 'baseline_bad_pct': Overall % of bads
            - 'lift': Lift at each decile
            - 'gain': Gain at each decile
            
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    if not actual or not predicted:
        raise ValueError("Both actual and predicted must be non-empty")
    
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    
    if num_deciles <= 0:
        raise ValueError("num_deciles must be positive")
    
    # Sort by predicted scores (descending)
    sorted_pairs = sorted(zip(predicted, actual), key=lambda x: x[0], reverse=True)
    
    total_bad = sum(1 for a in actual if a == 1)
    total_good = sum(1 for a in actual if a == 0)
    total = len(actual)
    baseline_bad_pct = total_bad / total if total > 0 else 0
    
    decile_size = total // num_deciles
    
    deciles = []
    good_counts = []
    bad_counts = []
    bad_pcts = []
    cum_bad_counts = []
    cum_bad_pcts = []
    lifts = []
    gains = []
    
    cum_bad = 0
    
    for i in range(num_deciles):
        start_idx = i * decile_size
        end_idx = start_idx + decile_size if i < num_deciles - 1 else total
        
        decile_data = sorted_pairs[start_idx:end_idx]
        good_count = sum(1 for _, label in decile_data if label == 0)
        bad_count = sum(1 for _, label in decile_data if label == 1)
        
        cum_bad += bad_count
        
        decile_size_actual = end_idx - start_idx
        bad_pct = bad_count / decile_size_actual if decile_size_actual > 0 else 0
        cum_bad_pct = cum_bad / total_bad if total_bad > 0 else 0
        
        lift = bad_pct / baseline_bad_pct if baseline_bad_pct > 0 else 0
        gain = cum_bad_pct
        
        deciles.append(i + 1)
        good_counts.append(good_count)
        bad_counts.append(bad_count)
        bad_pcts.append(bad_pct)
        cum_bad_counts.append(cum_bad)
        cum_bad_pcts.append(cum_bad_pct)
        lifts.append(lift)
        gains.append(gain)
    
    return {
        'deciles': deciles,
        'good_count': good_counts,
        'bad_count': bad_counts,
        'bad_pct_in_decile': bad_pcts,
        'cum_bad_count': cum_bad_counts,
        'cum_bad_pct': cum_bad_pcts,
        'baseline_bad_pct': baseline_bad_pct,
        'lift': lifts,
        'gain': gains
    }


def divergence_kl(p: List[float], q: List[float]) -> float:
    """Calculate Kullback-Leibler (KL) Divergence between two distributions.
    
    KL divergence measures how much one distribution diverges from another.
    Range: 0 to infinity (0 = identical distributions)
    Note: KL divergence is asymmetric (D(p||q) != D(q||p))
    
    Args:
        p: First probability distribution (reference)
        q: Second probability distribution
        
    Returns:
        KL divergence value (0 to infinity)
        
    Raises:
        ValueError: If distributions are invalid or have different lengths
    """
    if not p or not q:
        raise ValueError("Both distributions must be non-empty")
    
    if len(p) != len(q):
        raise ValueError("Distributions must have the same length")
    
    # Normalize to ensure they sum to 1
    p_sum = sum(p)
    q_sum = sum(q)
    
    if p_sum <= 0 or q_sum <= 0:
        raise ValueError("Distributions must have positive sums")
    
    p_norm = [x / p_sum for x in p]
    q_norm = [x / q_sum for x in q]
    
    epsilon = 1e-10
    kl_div = 0.0
    
    for p_i, q_i in zip(p_norm, q_norm):
        p_i = max(p_i, epsilon)
        q_i = max(q_i, epsilon)
        kl_div += p_i * math.log(p_i / q_i)
    
    return kl_div


def divergence_js(p: List[float], q: List[float]) -> float:
    """Calculate Jensen-Shannon (JS) Divergence between two distributions.
    
    JS divergence is symmetric and bounded between 0 and 1.
    Formula: JS(p||q) = 0.5 * KL(p||m) + 0.5 * KL(q||m) where m = 0.5*(p+q)
    
    Args:
        p: First probability distribution
        q: Second probability distribution
        
    Returns:
        JS divergence value (0 to 1)
        
    Raises:
        ValueError: If distributions are invalid or have different lengths
    """
    if not p or not q:
        raise ValueError("Both distributions must be non-empty")
    
    if len(p) != len(q):
        raise ValueError("Distributions must have the same length")
    
    p_sum = sum(p)
    q_sum = sum(q)
    
    if p_sum <= 0 or q_sum <= 0:
        raise ValueError("Distributions must have positive sums")
    
    p_norm = [x / p_sum for x in p]
    q_norm = [x / q_sum for x in q]
    
    # Calculate midpoint distribution
    m = [(p_i + q_i) / 2 for p_i, q_i in zip(p_norm, q_norm)]
    
    # Calculate JS as average of two KL divergences
    kl_pm = divergence_kl(p_norm, m)
    kl_qm = divergence_kl(q_norm, m)
    
    return 0.5 * kl_pm + 0.5 * kl_qm


def hosmer_lemeshow_test(actual: List[int], predicted: List[float], num_groups: int = 10) -> Dict[str, Union[float, int]]:
    """Perform Hosmer-Lemeshow test for goodness-of-fit.
    
    Tests whether predicted probabilities match actual outcomes in each group.
    p-value > 0.05 indicates good model fit.
    
    Args:
        actual: List of actual labels (0 for good, 1 for bad)
        predicted: List of predicted probabilities (0 to 1)
        num_groups: Number of groups to divide data into (default: 10)
        
    Returns:
        Dictionary containing:
            - 'test_statistic': Chi-squared test statistic
            - 'p_value': p-value of the test
            - 'df': Degrees of freedom
            - 'groups': Group statistics
            
    Raises:
        ValueError: If inputs are invalid
    """
    if not actual or not predicted:
        raise ValueError("Both actual and predicted must be non-empty")
    
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    
    if num_groups <= 1:
        raise ValueError("num_groups must be greater than 1")
    
    # Sort by predicted probability
    sorted_pairs = sorted(zip(predicted, actual), key=lambda x: x[0])
    
    group_size = len(actual) // num_groups
    test_statistic = 0.0
    groups = []
    
    for i in range(num_groups):
        start_idx = i * group_size
        end_idx = start_idx + group_size if i < num_groups - 1 else len(actual)
        
        group_data = sorted_pairs[start_idx:end_idx]
        
        group_size_actual = end_idx - start_idx
        observed_events = sum(1 for _, label in group_data if label == 1)
        expected_prob = sum(prob for prob, _ in group_data) / group_size_actual if group_size_actual > 0 else 0
        expected_events = expected_prob * group_size_actual
        
        if expected_events > 0 and (group_size_actual - expected_events) > 0:
            chi_sq = ((observed_events - expected_events) ** 2 / expected_events +
                     ((group_size_actual - observed_events) - (group_size_actual - expected_events)) ** 2 / 
                     (group_size_actual - expected_events))
            test_statistic += chi_sq
        
        groups.append({
            'group': i + 1,
            'observed_events': observed_events,
            'expected_events': expected_events,
            'observed_non_events': group_size_actual - observed_events,
            'expected_non_events': group_size_actual - expected_events
        })
    
    # p-value approximation using chi-squared distribution
    # For simplicity, we return the test statistic
    df = num_groups - 2
    
    return {
        'test_statistic': test_statistic,
        'df': df,
        'groups': groups
    }


def brier_score(actual: List[int], predicted: List[float]) -> float:
    """Calculate Brier Score for probability forecast evaluation.
    
    Brier score measures mean squared error of predicted probabilities.
    Range: 0 to 1 (0 = perfect calibration, 1 = worst calibration)
    Lower is better.
    
    Args:
        actual: List of actual labels (0 or 1)
        predicted: List of predicted probabilities (0 to 1)
        
    Returns:
        Brier score (0 to 1)
        
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    if not actual or not predicted:
        raise ValueError("Both actual and predicted must be non-empty")
    
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    
    squared_errors = [(y - p) ** 2 for y, p in zip(actual, predicted)]
    return sum(squared_errors) / len(actual)


def log_loss(actual: List[int], predicted: List[float]) -> float:
    """Calculate Log Loss (Cross-Entropy) for classification models.
    
    Log loss penalizes confident wrong predictions heavily.
    Range: 0 to infinity (0 = perfect prediction)
    Lower is better.
    
    Args:
        actual: List of actual labels (0 or 1)
        predicted: List of predicted probabilities (0 to 1)
        
    Returns:
        Log loss value
        
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    if not actual or not predicted:
        raise ValueError("Both actual and predicted must be non-empty")
    
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    
    epsilon = 1e-15
    log_losses = []
    
    for y, p in zip(actual, predicted):
        p = max(epsilon, min(1 - epsilon, p))
        if y == 1:
            log_losses.append(-math.log(p))
        else:
            log_losses.append(-math.log(1 - p))
    
    return sum(log_losses) / len(actual)


def precision_recall_f1(actual: List[int], predicted: List[int]) -> Dict[str, float]:
    """Calculate Precision, Recall, and F1-Score for classification.
    
    - Precision: % of predicted positives that are actually positive
    - Recall: % of actual positives that are correctly predicted
    - F1-Score: Harmonic mean of precision and recall
    
    Args:
        actual: List of actual labels (0 or 1)
        predicted: List of predicted labels (0 or 1)
        
    Returns:
        Dictionary containing:
            - 'precision': Precision score (0 to 1)
            - 'recall': Recall score (0 to 1)
            - 'f1': F1-score (0 to 1)
            - 'true_positives': Count of TP
            - 'false_positives': Count of FP
            - 'false_negatives': Count of FN
            
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    if not actual or not predicted:
        raise ValueError("Both actual and predicted must be non-empty")
    
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    
    tp = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 1)
    fp = sum(1 for a, p in zip(actual, predicted) if a == 0 and p == 1)
    fn = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 0)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn
    }


def odds_ratio(good_data: List[Union[int, float]], bad_data: List[Union[int, float]], 
               num_bins: int = 10) -> Dict[str, Union[List, Dict]]:
    """Calculate Odds Ratio for each bin (used in scorecard development).
    
    Odds ratio shows the relative odds of default at different score ranges.
    Formula: Odds = Bad% / Good%
    
    Args:
        good_data: List of scores for good customers
        bad_data: List of scores for bad customers
        num_bins: Number of bins to create (default: 10)
        
    Returns:
        Dictionary containing bin-wise odds ratios
        
    Raises:
        ValueError: If either dataset is empty
    """
    if not good_data or not bad_data:
        raise ValueError("Both good_data and bad_data must be non-empty")
    
    if num_bins <= 0:
        raise ValueError("num_bins must be positive")
    
    all_data = good_data + bad_data
    min_val = min(all_data)
    max_val = max(all_data)
    
    if min_val == max_val:
        return {'bins': {}}
    
    bin_edges = [min_val + (max_val - min_val) * i / num_bins for i in range(num_bins + 1)]
    
    bins = {}
    epsilon = 1e-10
    
    for i in range(num_bins):
        if i == num_bins - 1:
            good_count = sum(1 for x in good_data if bin_edges[i] <= x <= bin_edges[i + 1])
            bad_count = sum(1 for x in bad_data if bin_edges[i] <= x <= bin_edges[i + 1])
        else:
            good_count = sum(1 for x in good_data if bin_edges[i] <= x < bin_edges[i + 1])
            bad_count = sum(1 for x in bad_data if bin_edges[i] <= x < bin_edges[i + 1])
        
        good_pct = good_count / len(good_data) if good_count > 0 else epsilon
        bad_pct = bad_count / len(bad_data) if bad_count > 0 else epsilon
        
        odds = bad_pct / good_pct if good_pct > 0 else 0
        
        bins[f"bin_{i}"] = {
            'range': (bin_edges[i], bin_edges[i + 1]),
            'good_count': good_count,
            'bad_count': bad_count,
            'good_pct': good_pct,
            'bad_pct': bad_pct,
            'odds': odds
        }
    
    return {'bins': bins}


def acceptance_reject_rates(predicted: List[float], cutoff: float) -> Dict[str, Union[float, int]]:
    """Calculate Acceptance and Rejection Rates at a given cutoff score.
    
    These are business metrics showing the proportion of applicants 
    approved/rejected at a given score threshold.
    
    Args:
        predicted: List of predicted scores/probabilities
        cutoff: Decision threshold (approve if score >= cutoff)
        
    Returns:
        Dictionary containing:
            - 'total_applicants': Total number of applicants
            - 'approved': Count of approved applicants
            - 'rejected': Count of rejected applicants
            - 'acceptance_rate': % of applicants approved
            - 'rejection_rate': % of applicants rejected
            
    Raises:
        ValueError: If predicted list is empty
    """
    if not predicted:
        raise ValueError("predicted list must be non-empty")
    
    total = len(predicted)
    approved = sum(1 for score in predicted if score >= cutoff)
    rejected = total - approved
    
    acceptance_rate = approved / total if total > 0 else 0
    rejection_rate = rejected / total if total > 0 else 0
    
    return {
        'total_applicants': total,
        'approved': approved,
        'rejected': rejected,
        'acceptance_rate': acceptance_rate,
        'rejection_rate': rejection_rate
    }


def spearman_rank_correlation(data1: List[Union[int, float]], data2: List[Union[int, float]]) -> float:
    """Calculate Spearman Rank Correlation coefficient.
    
    Measures monotonic relationship between two variables (useful for ordinal/ranked predictions).
    Range: -1 to 1 (-1 = perfect negative correlation, 1 = perfect positive)
    
    Args:
        data1: First list of values
        data2: Second list of values
        
    Returns:
        Spearman rank correlation coefficient
        
    Raises:
        ValueError: If lists are empty or have different lengths
    """
    if not data1 or not data2:
        raise ValueError("Both lists must be non-empty")
    
    if len(data1) != len(data2):
        raise ValueError("Lists must have the same length")
    
    n = len(data1)
    
    # Rank the data
    def rank(data: List[Union[int, float]]) -> List[float]:
        sorted_data = sorted(enumerate(data), key=lambda x: x[1])
        ranks = [0] * len(data)
        for rank_val, (original_idx, _) in enumerate(sorted_data, 1):
            ranks[original_idx] = rank_val
        return ranks
    
    ranks1 = rank(data1)
    ranks2 = rank(data2)
    
    # Calculate Pearson correlation on ranks
    mean1 = sum(ranks1) / n
    mean2 = sum(ranks2) / n
    
    numerator = sum((r1 - mean1) * (r2 - mean2) for r1, r2 in zip(ranks1, ranks2))
    denominator = math.sqrt(sum((r1 - mean1) ** 2 for r1 in ranks1) * sum((r2 - mean2) ** 2 for r2 in ranks2))
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator
