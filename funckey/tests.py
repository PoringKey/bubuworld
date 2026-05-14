"""Unit tests for funckey statistical functions."""

import unittest
from funckey.stats import (
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
)


class TestStatisticalFunctions(unittest.TestCase):
    """Test cases for statistical functions."""
    
    def setUp(self):
        """Set up test data."""
        self.data1 = [1, 2, 3, 4, 5]
        self.data2 = [2, 4, 6, 8, 10]
        self.data_with_duplicates = [1, 2, 2, 3, 3, 3, 4]
    
    def test_mean(self):
        """Test mean calculation."""
        self.assertEqual(mean(self.data1), 3.0)
        self.assertEqual(mean(self.data2), 6.0)
    
    def test_median(self):
        """Test median calculation."""
        self.assertEqual(median(self.data1), 3)
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
    
    def test_mode(self):
        """Test mode calculation."""
        self.assertEqual(mode(self.data_with_duplicates), 3)
    
    def test_variance(self):
        """Test variance calculation."""
        var = variance(self.data1)
        self.assertAlmostEqual(var, 2.0)
    
    def test_std_dev(self):
        """Test standard deviation calculation."""
        std = std_dev(self.data1)
        self.assertAlmostEqual(std, 1.4142135623730951)
    
    def test_min_max(self):
        """Test min and max functions."""
        self.assertEqual(min_value(self.data1), 1)
        self.assertEqual(max_value(self.data1), 5)
    
    def test_range(self):
        """Test range calculation."""
        self.assertEqual(range_value(self.data1), 4)
    
    def test_quartiles(self):
        """Test quartiles calculation."""
        q1, q2, q3 = quartiles(self.data1)
        self.assertEqual(q2, 3)  # Median
    
    def test_covariance(self):
        """Test covariance calculation."""
        cov = covariance(self.data1, self.data2)
        self.assertAlmostEqual(cov, 5.0)
    
    def test_correlation(self):
        """Test correlation calculation."""
        corr = correlation(self.data1, self.data2)
        self.assertAlmostEqual(corr, 1.0)  # Perfect positive correlation
    
    def test_empty_dataset_error(self):
        """Test that empty datasets raise ValueError."""
        with self.assertRaises(ValueError):
            mean([])
        with self.assertRaises(ValueError):
            median([])
        with self.assertRaises(ValueError):
            min_value([])


if __name__ == "__main__":
    unittest.main()
