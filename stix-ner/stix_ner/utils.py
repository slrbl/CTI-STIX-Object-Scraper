# utility functions here
def classification_metrics_from_counts(tp, fp, tn, fn):
    """
    Calculate precision, recall, F1-score, and accuracy from confusion matrix counts.

    Parameters:
        tp (int): True Positives
        fp (int): False Positives
        tn (int): True Negatives
        fn (int): False Negatives

    Returns:
        dict: Dictionary containing precision, recall, f1-score, and accuracy
    """
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) != 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'accuracy': accuracy
    }