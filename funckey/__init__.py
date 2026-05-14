"""funckey - A Python library for standard statistical functions and credit scoring metrics."""

from funckey.stats import (
    # Basic statistics
    mean,
    median,
    mode,
    variance,
    std_dev,
    min_value,
    max_value,
    range_value,
    quartiles,
    correlation,
    covariance,
    # Credit scoring metrics
    ks_statistic,
    psi,
    psi_by_bins,
    iv_statistic,
    auc_score,
    gini_coefficient,
    somers_d,
    lift_gain,
    divergence_kl,
    divergence_js,
    hosmer_lemeshow_test,
    brier_score,
    log_loss,
    precision_recall_f1,
    odds_ratio,
    acceptance_reject_rates,
    spearman_rank_correlation,
)

# Try to import optbinning for advanced binning capabilities
try:
    from optbinning import OptimalBinning, OptimalBinning2D, BinningProcess
    HAS_OPTBINNING = True
except ImportError:
    HAS_OPTBINNING = False

__version__ = "0.2.0"
__author__ = "PoringKey"

__all__ = [
    # Basic statistics
    "mean",
    "median",
    "mode",
    "variance",
    "std_dev",
    "min_value",
    "max_value",
    "range_value",
    "quartiles",
    "correlation",
    "covariance",
    # Credit scoring metrics - Distribution metrics
    "ks_statistic",
    "psi",
    "psi_by_bins",
    "iv_statistic",
    # Credit scoring metrics - Classification metrics
    "auc_score",
    "gini_coefficient",
    "somers_d",
    "lift_gain",
    # Credit scoring metrics - Distribution comparison
    "divergence_kl",
    "divergence_js",
    # Credit scoring metrics - Calibration metrics
    "hosmer_lemeshow_test",
    "brier_score",
    "log_loss",
    # Credit scoring metrics - Classification metrics
    "precision_recall_f1",
    # Credit scoring metrics - Business metrics
    "odds_ratio",
    "acceptance_reject_rates",
    # Credit scoring metrics - Correlation metrics
    "spearman_rank_correlation",
    # optbinning integration (optional)
    "HAS_OPTBINNING",
]

# If optbinning is available, add it to exports
if HAS_OPTBINNING:
    __all__.extend(["OptimalBinning", "OptimalBinning2D", "BinningProcess"])
