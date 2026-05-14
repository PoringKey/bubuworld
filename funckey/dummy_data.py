"""Dummy dataset for credit scoring model development and testing."""

import random
from typing import Tuple, List, Dict
import json


def generate_credit_scoring_dataset(
    n_samples: int = 1000,
    default_rate: float = 0.15,
    seed: int = 42
) -> Dict[str, List]:
    """Generate synthetic credit scoring dataset.
    
    Creates a realistic dummy dataset with features commonly used in credit scoring models.
    Default rate is typically between 10-20% in real datasets.
    
    Args:
        n_samples: Number of samples to generate (default: 1000)
        default_rate: Proportion of defaults (0 to 1, default: 0.15 = 15%)
        seed: Random seed for reproducibility (default: 42)
        
    Returns:
        Dictionary containing:
            - 'age': Applicant age (20-75)
            - 'income': Annual income (20000-250000)
            - 'credit_score': Credit bureau score (300-850)
            - 'employment_years': Years at current employer (0-40)
            - 'debt_to_income': Debt to income ratio (0-100%)
            - 'num_inquiries': Number of credit inquiries in last 6 months (0-10)
            - 'default': Target variable (0=good, 1=bad/default)
    """
    random.seed(seed)
    
    n_defaults = int(n_samples * default_rate)
    n_goods = n_samples - n_defaults
    
    dataset = {
        'age': [],
        'income': [],
        'credit_score': [],
        'employment_years': [],
        'debt_to_income': [],
        'num_inquiries': [],
        'num_accounts': [],
        'utilization_rate': [],
        'payment_history': [],
        'default': []
    }
    
    # Generate good customers (default=0)
    for _ in range(n_goods):
        age = random.randint(25, 70)
        income = random.randint(30000, 250000)
        credit_score = random.randint(650, 850)  # Higher scores for good customers
        employment_years = random.randint(0, 30)
        debt_to_income = round(random.uniform(5, 50), 2)  # Lower DTI for good
        num_inquiries = random.randint(0, 3)
        num_accounts = random.randint(2, 8)
        utilization_rate = round(random.uniform(10, 60), 2)
        payment_history = round(random.uniform(90, 100), 2)
        
        dataset['age'].append(age)
        dataset['income'].append(income)
        dataset['credit_score'].append(credit_score)
        dataset['employment_years'].append(employment_years)
        dataset['debt_to_income'].append(debt_to_income)
        dataset['num_inquiries'].append(num_inquiries)
        dataset['num_accounts'].append(num_accounts)
        dataset['utilization_rate'].append(utilization_rate)
        dataset['payment_history'].append(payment_history)
        dataset['default'].append(0)
    
    # Generate bad customers (default=1)
    for _ in range(n_defaults):
        age = random.randint(22, 75)
        income = random.randint(20000, 150000)
        credit_score = random.randint(300, 650)  # Lower scores for bad customers
        employment_years = random.randint(0, 15)
        debt_to_income = round(random.uniform(50, 100), 2)  # Higher DTI for bad
        num_inquiries = random.randint(4, 10)  # More inquiries for bad
        num_accounts = random.randint(1, 6)
        utilization_rate = round(random.uniform(70, 100), 2)
        payment_history = round(random.uniform(60, 95), 2)
        
        dataset['age'].append(age)
        dataset['income'].append(income)
        dataset['credit_score'].append(credit_score)
        dataset['employment_years'].append(employment_years)
        dataset['debt_to_income'].append(debt_to_income)
        dataset['num_inquiries'].append(num_inquiries)
        dataset['num_accounts'].append(num_accounts)
        dataset['utilization_rate'].append(utilization_rate)
        dataset['payment_history'].append(payment_history)
        dataset['default'].append(1)
    
    # Shuffle the data
    indices = list(range(n_samples))
    random.shuffle(indices)
    
    shuffled_dataset = {}
    for key in dataset.keys():
        shuffled_dataset[key] = [dataset[key][i] for i in indices]
    
    return shuffled_dataset


def save_dataset_to_json(dataset: Dict[str, List], filepath: str = "credit_data.json") -> None:
    """Save dataset to JSON file.
    
    Args:
        dataset: Dictionary containing the dataset
        filepath: Path to save the JSON file
    """
    with open(filepath, 'w') as f:
        json.dump(dataset, f, indent=2)
    print(f"Dataset saved to {filepath}")


def load_dataset_from_json(filepath: str = "credit_data.json") -> Dict[str, List]:
    """Load dataset from JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary containing the dataset
    """
    with open(filepath, 'r') as f:
        dataset = json.load(f)
    print(f"Dataset loaded from {filepath}")
    return dataset


def print_dataset_summary(dataset: Dict[str, List]) -> None:
    """Print summary statistics of the dataset.
    
    Args:
        dataset: Dictionary containing the dataset
    """
    print("\n" + "="*70)
    print("DATASET SUMMARY".center(70))
    print("="*70)
    
    n_samples = len(dataset['default'])
    n_defaults = sum(dataset['default'])
    n_goods = n_samples - n_defaults
    default_rate = n_defaults / n_samples if n_samples > 0 else 0
    
    print(f"\nTotal Samples: {n_samples}")
    print(f"Good Customers (0): {n_goods} ({n_goods/n_samples*100:.2f}%)")
    print(f"Bad Customers (1): {n_defaults} ({n_defaults/n_samples*100:.2f}%)")
    print(f"Default Rate: {default_rate*100:.2f}%")
    
    print("\n" + "-"*70)
    print("FEATURE STATISTICS".center(70))
    print("-"*70)
    
    for key in dataset.keys():
        if key != 'default':
            values = dataset[key]
            print(f"\n{key.upper()}:")
            print(f"  Min: {min(values):.2f}, Max: {max(values):.2f}, "
                  f"Mean: {sum(values)/len(values):.2f}")


if __name__ == "__main__":
    # Generate sample dataset
    print("Generating credit scoring dataset...")
    dataset = generate_credit_scoring_dataset(n_samples=1000, default_rate=0.15)
    
    # Print summary
    print_dataset_summary(dataset)
    
    # Save to JSON
    save_dataset_to_json(dataset, "credit_data.json")
    
    print("\n✓ Dataset generated successfully!")
