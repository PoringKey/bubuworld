# funckey

A Python library for standard statistical functions.

## Features

- **Central Tendency**: mean, median, mode
- **Dispersion**: variance, standard deviation, range
- **Distribution**: quartiles
- **Relationships**: covariance, correlation
- **Extremes**: minimum, maximum

## Installation

```bash
pip install funckey
```

## Usage

```python
from funckey import mean, median, std_dev, correlation

data = [1, 2, 3, 4, 5]
print(mean(data))  # 3.0
print(median(data))  # 3
print(std_dev(data))  # 1.414...

# Calculate correlation between two datasets
data1 = [1, 2, 3, 4, 5]
data2 = [2, 4, 6, 8, 10]
corr = correlation(data1, data2)  # 1.0 (perfect positive correlation)
```

## API Reference

### Central Tendency

- `mean(data)` - Calculate arithmetic mean
- `median(data)` - Calculate median
- `mode(data)` - Calculate mode (most frequent value)

### Dispersion

- `variance(data, sample=False)` - Calculate variance
- `std_dev(data, sample=False)` - Calculate standard deviation
- `range_value(data)` - Calculate range (max - min)

### Distribution

- `quartiles(data)` - Calculate Q1, Q2 (median), Q3

### Extremes

- `min_value(data)` - Find minimum value
- `max_value(data)` - Find maximum value

### Relationships

- `covariance(data1, data2, sample=False)` - Calculate covariance
- `correlation(data1, data2)` - Calculate Pearson correlation coefficient

## Testing

Run the test suite:

```bash
python -m funckey.tests
```

## License

MIT
