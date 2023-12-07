import copy

import numpy as np


class LinearRegression:

    def __init__(self):
        pass

    def _cost(self, x, y, w, b, lambda_=None):
        m = x.shape[0]
        fx = np.dot(x, w) + b
        jwb = np.sum(np.square(fx - y)) / (2 * m)
        if lambda_:
            jwb += lambda_ * np.sum(w ** 2) / (2 * m)
        return jwb

    def _gradient_descent(self, x, y, w, b, lambda_=None):
        m = x.shape[0]
        fx = np.dot(x, w) + b
        dw = np.sum(np.dot((fx - y), x)) / m
        if lambda_:
            dw += lambda_ * w / m
        db = np.sum(fx - y) / m
        return dw, db

    def train(self, x, y, w_init, b_init, alpha, iterations, lambda_):
        cost_history = []
        parameters_history = []

        w = copy.deepcopy(w_init)
        b = copy.deepcopy(b_init)

        for i in range(iterations):
            dw, db = self._gradient_descent(x, y, w, b, lambda_)
            w = w - alpha * dw
            b = b - alpha * db

            if i < 100000:
                cost_history.append(self._cost(x, y, w, b, lambda_))
                parameters_history.append([w, b])

        return w, b, cost_history, parameters_history

    def predict(self, x, w, b):
        return np.dot(x, w) + b
