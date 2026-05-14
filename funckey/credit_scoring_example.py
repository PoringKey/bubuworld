"""Example script demonstrating how to use funckey for credit scoring model evaluation.

This script shows:
1. Loading/generating sample credit scoring data
2. Creating a simple logistic regression model
3. Evaluating the model using various credit scoring metrics
4. Interpreting the results
"""

import sys
import random
from typing import List, Dict, Tuple

# Import from funckey
from funckey.dummy_data import generate_credit_scoring_dataset, print_dataset_summary
from funckey import (
    # Classification metrics
    ks_statistic,
    auc_score,
    gini_coefficient,
    somers_d,
    # Distribution metrics
    psi_by_bins,
    iv_statistic,
    # Business metrics
    lift_gain,
    odds_ratio,
    acceptance_reject_rates,
    # Calibration metrics
    brier_score,
    log_loss,
    hosmer_lemeshow_test,
    # Classification metrics
    precision_recall_f1,
    # Divergence metrics
    divergence_kl,
    divergence_js,
    # Correlation metrics
    spearman_rank_correlation,
)


class SimpleLogisticRegression:
    """Simple logistic regression model for credit scoring (for demonstration)."""
    
    def __init__(self):
        """Initialize the model."""
        self.weights = {}
        self.intercept = 0.0
    
    def fit(self, X: Dict[str, List], y: List[int]) -> None:
        """Fit the model using simple heuristics based on feature correlations.
        
        Args:
            X: Dictionary of feature lists
            y: Target variable (0=good, 1=bad)
        """
        # Simple correlation-based weights (for demo purposes)
        self.intercept = -2.0
        
        # Features that increase default risk (positive correlation with default)
        self.weights = {
            'age': -0.02,  # Older customers are less risky
            'income': -0.00001,  # Higher income is less risky
            'credit_score': -0.01,  # Higher credit score is less risky
            'employment_years': -0.05,  # More employment is less risky
            'debt_to_income': 0.03,  # Higher DTI increases risk
            'num_inquiries': 0.2,  # More inquiries increase risk
            'num_accounts': -0.1,  # More accounts decrease risk (diversification)
            'utilization_rate': 0.02,  # Higher utilization increases risk
            'payment_history': -0.05,  # Better payment history decreases risk
        }
    
    def predict_proba(self, X: Dict[str, List]) -> List[float]:
        """Predict probability of default.
        
        Args:
            X: Dictionary of feature lists
            
        Returns:
            List of predicted probabilities (0 to 1)
        """
        predictions = []
        n_samples = len(X[list(X.keys())[0]])
        
        for i in range(n_samples):
            score = self.intercept
            for feature, weight in self.weights.items():
                if feature in X:
                    # Normalize feature to 0-1 range for consistent weighting
                    min_val = min(X[feature])
                    max_val = max(X[feature])
                    if max_val > min_val:
                        normalized = (X[feature][i] - min_val) / (max_val - min_val)
                    else:
                        normalized = 0.5
                    score += weight * normalized
            
            # Sigmoid function to convert score to probability
            prob = 1.0 / (1.0 + (2.718281828 ** (-score)))
            predictions.append(prob)
        
        return predictions
    
    def predict(self, X: Dict[str, List], threshold: float = 0.5) -> List[int]:
        """Predict binary class (0 or 1).
        
        Args:
            X: Dictionary of feature lists
            threshold: Decision threshold
            
        Returns:
            List of predicted labels (0 or 1)
        """
        probabilities = self.predict_proba(X)
        return [1 if p >= threshold else 0 for p in probabilities]


def main():
    """Run the complete credit scoring example."""
    
    print("\n" + "="*80)
    print("CREDIT SCORING MODEL EVALUATION - FUNCKEY LIBRARY DEMO".center(80))
    print("="*80)
    
    # Step 1: Generate data
    print("\n[STEP 1] Generating synthetic credit scoring dataset...")
    dataset = generate_credit_scoring_dataset(n_samples=1000, default_rate=0.15, seed=42)
    print_dataset_summary(dataset)
    
    # Step 2: Split data (80-20 split)
    print("\n[STEP 2] Splitting data into train (80%) and test (20%)...")
    n_train = int(len(dataset['default']) * 0.8)
    
    train_X = {key: dataset[key][:n_train] for key in dataset.keys() if key != 'default'}
    train_y = dataset['default'][:n_train]
    
    test_X = {key: dataset[key][n_train:] for key in dataset.keys() if key != 'default'}
    test_y = dataset['default'][n_train:]
    
    print(f"Training set: {len(train_y)} samples")
    print(f"Test set: {len(test_y)} samples")
    
    # Step 3: Train model
    print("\n[STEP 3] Training logistic regression model...")
    model = SimpleLogisticRegression()
    model.fit(train_X, train_y)
    print("✓ Model trained")
    
    # Step 4: Make predictions
    print("\n[STEP 4] Making predictions on test set...")
    test_pred_proba = model.predict_proba(test_X)
    test_pred_labels = model.predict(test_X, threshold=0.5)
    print(f"✓ Predictions made: {len(test_pred_proba)} samples")
    
    # Step 5: Evaluate model using credit scoring metrics
    print("\n" + "="*80)
    print("[STEP 5] MODEL EVALUATION - CREDIT SCORING METRICS".center(80))
    print("="*80)
    
    # Separate good and bad predictions for KS statistic
    good_scores = [test_pred_proba[i] for i in range(len(test_y)) if test_y[i] == 0]
    bad_scores = [test_pred_proba[i] for i in range(len(test_y)) if test_y[i] == 1]
    
    # A. DISCRIMINATION METRICS
    print("\n" + "-"*80)
    print("A. DISCRIMINATION METRICS (How well does the model separate good from bad?)".ljust(80))
    print("-"*80)
    
    # KS Statistic
    ks_result = ks_statistic(good_scores, bad_scores)
    print(f"\n1. Kolmogorov-Smirnov (KS) Statistic: {ks_result['ks_statistic']:.4f}")
    print(f"   Interpretation: {interpret_ks(ks_result['ks_statistic'])}")
    
    # AUC Score
    auc = auc_score(test_y, test_pred_proba)
    print(f"\n2. Area Under ROC Curve (AUC): {auc:.4f}")
    print(f"   Interpretation: {interpret_auc(auc)}")
    
    # Gini Coefficient
    gini = gini_coefficient(test_y, test_pred_proba)
    print(f"\n3. Gini Coefficient: {gini:.4f}")
    print(f"   Interpretation: {interpret_gini(gini)}")
    
    # Somers' D
    somers = somers_d(test_y, test_pred_proba)
    print(f"\n4. Somers' D Statistic: {somers:.4f}")
    print(f"   Interpretation: {interpret_somers(somers)}")
    
    # B. FEATURE IMPORTANCE METRICS
    print("\n" + "-"*80)
    print("B. FEATURE IMPORTANCE METRICS (Which features matter most?)".ljust(80))
    print("-"*80)
    
    # Information Value for Credit Score
    iv_credit = iv_statistic(good_scores, bad_scores, num_bins=10)
    print(f"\n1. Information Value (IV): {iv_credit['iv']:.4f}")
    print(f"   Interpretation: {interpret_iv(iv_credit['iv'])}")
    
    # C. STABILITY METRICS
    print("\n" + "-"*80)
    print("C. STABILITY METRICS (Is the model stable over time?)".ljust(80))
    print("-"*80)
    
    # PSI - Compare train vs test predictions
    train_pred_proba = model.predict_proba(train_X)
    psi_value = psi_by_bins(train_pred_proba, test_pred_proba, num_bins=10)
    print(f"\n1. Population Stability Index (PSI): {psi_value:.4f}")
    print(f"   Interpretation: {interpret_psi(psi_value)}")
    
    # D. BUSINESS METRICS
    print("\n" + "-"*80)
    print("D. BUSINESS METRICS (What are the business implications?)".ljust(80))
    print("-"*80)
    
    # Lift and Gain
    lift_result = lift_gain(test_y, test_pred_proba, num_deciles=10)
    print(f"\n1. Lift Chart (by deciles):")
    print(f"   Decile 1 (Top 10%) Lift: {lift_result['lift'][0]:.2f}x")
    print(f"   Interpretation: Top 10% of applicants are {lift_result['lift'][0]:.2f}x more likely to default")
    print(f"   Decile 1 Cumulative Default %: {lift_result['cum_bad_pct'][0]*100:.2f}%")
    
    # Acceptance/Rejection Rates at different cutoffs
    print(f"\n2. Acceptance/Rejection Rates:")
    for cutoff in [0.3, 0.5, 0.7]:
        ar_result = acceptance_reject_rates(test_pred_proba, cutoff)
        print(f"   At cutoff {cutoff}: Accept {ar_result['acceptance_rate']*100:.1f}%, Reject {ar_result['rejection_rate']*100:.1f}%")
    
    # Odds Ratio
    odds_result = odds_ratio(good_scores, bad_scores, num_bins=5)
    print(f"\n3. Odds Ratio by Score Bins:")
    for bin_name, bin_data in odds_result['bins'].items():
        if bin_data['good_pct'] > 0:
            print(f"   {bin_name}: Odds = {bin_data['odds']:.3f}")
    
    # E. CALIBRATION METRICS
    print("\n" + "-"*80)
    print("E. CALIBRATION METRICS (Are predicted probabilities accurate?)".ljust(80))
    print("-"*80)
    
    # Brier Score
    brier = brier_score(test_y, test_pred_proba)
    print(f"\n1. Brier Score: {brier:.4f}")
    print(f"   Interpretation: {interpret_brier(brier)}")
    
    # Log Loss
    logloss = log_loss(test_y, test_pred_proba)
    print(f"\n2. Log Loss: {logloss:.4f}")
    print(f"   Interpretation: Lower is better. Perfect prediction = 0.")
    
    # Hosmer-Lemeshow Test
    hl_result = hosmer_lemeshow_test(test_y, test_pred_proba, num_groups=10)
    print(f"\n3. Hosmer-Lemeshow Test:")
    print(f"   Chi-squared statistic: {hl_result['test_statistic']:.4f}")
    print(f"   p-value > 0.05 indicates good fit (model is well-calibrated)")
    
    # F. CLASSIFICATION METRICS
    print("\n" + "-"*80)
    print("F. CLASSIFICATION METRICS (At threshold = 0.5)".ljust(80))
    print("-"*80)
    
    prf = precision_recall_f1(test_y, test_pred_labels)
    print(f"\n1. Precision: {prf['precision']:.4f}")
    print(f"   Interpretation: {prf['true_positives']} out of {prf['true_positives'] + prf['false_positives']} predicted defaults are actually defaults")
    
    print(f"\n2. Recall: {prf['recall']:.4f}")
    print(f"   Interpretation: Caught {prf['true_positives']} out of {prf['true_positives'] + prf['false_negatives']} actual defaults")
    
    print(f"\n3. F1-Score: {prf['f1']:.4f}")
    print(f"   Interpretation: Harmonic mean of precision and recall (0-1, higher is better)")
    
    # G. DISTRIBUTION COMPARISON
    print("\n" + "-"*80)
    print("G. DISTRIBUTION COMPARISON METRICS".ljust(80))
    print("-"*80)
    
    # KL Divergence
    good_dist = [x / sum(good_scores) if x > 0 else 1e-10 for x in good_scores]
    bad_dist = [x / sum(bad_scores) if x > 0 else 1e-10 for x in bad_scores]
    
    if len(good_dist) == len(bad_dist):
        kl_div = divergence_kl(good_dist, bad_dist)
        print(f"\n1. KL Divergence: {kl_div:.4f}")
        print(f"   Interpretation: Measures divergence between good and bad distributions (0 = identical)")
    
    # H. CORRELATION ANALYSIS
    print("\n" + "-"*80)
    print("H. CORRELATION ANALYSIS".ljust(80))
    print("-"*80)
    
    spearman = spearman_rank_correlation(test_pred_proba, test_y)
    print(f"\n1. Spearman Rank Correlation: {spearman:.4f}")
    print(f"   Interpretation: Monotonic relationship between predictions and actual defaults")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY & RECOMMENDATIONS".center(80))
    print("="*80)
    
    print(f"""
    Model Performance Summary:
    ├─ AUC: {auc:.4f} ({interpret_auc(auc)})
    ├─ Gini: {gini:.4f} ({interpret_gini(gini)})
    ├─ KS Statistic: {ks_result['ks_statistic']:.4f} ({interpret_ks(ks_result['ks_statistic'])})
    ├─ PSI: {psi_value:.4f} ({interpret_psi(psi_value)})
    └─ IV: {iv_credit['iv']:.4f} ({interpret_iv(iv_credit['iv'])})
    
    Model Stability:
    └─ PSI < 0.1: Consider the model stable ({"✓" if psi_value < 0.1 else "✗"})
    
    Recommendations:
    """)
    
    if auc < 0.6:
        print("    • AUC is low - consider improving feature engineering or model complexity")
    if psi_value > 0.25:
        print("    • High PSI detected - monitor model and consider retraining")
    if brier > 0.25:
        print("    • Brier score indicates poor calibration - recalibrate predictions")
    
    print("\n" + "="*80)
    print("✓ Credit scoring evaluation complete!".center(80))
    print("="*80 + "\n")


def interpret_ks(ks_value: float) -> str:
    """Interpret KS statistic value."""
    if ks_value < 0.2:
        return "Poor discrimination"
    elif ks_value < 0.3:
        return "Fair discrimination"
    elif ks_value < 0.4:
        return "Good discrimination"
    else:
        return "Excellent discrimination"


def interpret_auc(auc_value: float) -> str:
    """Interpret AUC value."""
    if auc_value < 0.6:
        return "Poor"
    elif auc_value < 0.7:
        return "Fair"
    elif auc_value < 0.8:
        return "Good"
    else:
        return "Excellent"


def interpret_gini(gini_value: float) -> str:
    """Interpret Gini coefficient value."""
    if gini_value < 0.2:
        return "Poor"
    elif gini_value < 0.4:
        return "Fair"
    elif gini_value < 0.6:
        return "Good"
    else:
        return "Excellent"


def interpret_somers(somers_value: float) -> str:
    """Interpret Somers' D value."""
    if abs(somers_value) < 0.2:
        return "Weak association"
    elif abs(somers_value) < 0.4:
        return "Moderate association"
    else:
        return "Strong association"


def interpret_iv(iv_value: float) -> str:
    """Interpret Information Value."""
    if iv_value < 0.02:
        return "Not useful"
    elif iv_value < 0.1:
        return "Weak predictive power"
    elif iv_value < 0.3:
        return "Medium predictive power"
    elif iv_value < 0.5:
        return "Strong predictive power"
    else:
        return "Excellent predictive power"


def interpret_psi(psi_value: float) -> str:
    """Interpret Population Stability Index."""
    if psi_value < 0.1:
        return "Negligible population change"
    elif psi_value < 0.25:
        return "Small population change"
    else:
        return "Significant population change (consider retraining)"


def interpret_brier(brier_value: float) -> str:
    """Interpret Brier Score."""
    if brier_value < 0.15:
        return "Excellent calibration"
    elif brier_value < 0.25:
        return "Good calibration"
    else:
        return "Poor calibration"


if __name__ == "__main__":
    main()
