import numpy as np


def divide_by_max(x):
    x_scaled = (x - x.min()) / x.max()
    return x_scaled


def mean_normalization(x):
    mu = np.mean(x, axis=0)
    x_scaled = (x - mu) / (x.max() - x.min())
    return x_scaled


def z_score_normalization(x):
    mu = np.mean(x, axis=0)
    sigma = np.std(x, axis=0)
    x_scaled = (x - mu) / sigma
    return x_scaled
