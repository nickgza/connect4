import numpy as np

def mean_squared(y_expected: np.ndarray, y_predicted: np.ndarray) -> np.number:
    return np.mean((y_expected - y_predicted) ** 2)

def d_mean_squared(y_expected: np.ndarray, y_predicted: np.ndarray) -> np.ndarray:
    return 2 / np.size(y_expected) * (y_predicted - y_expected)
