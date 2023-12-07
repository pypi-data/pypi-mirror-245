import numpy as np
from customllib.supervised.regression.linear_regression import LinearRegression
from customllib.utils.feature_scaling import z_score_normalization

data = np.loadtxt("data/houses.txt", delimiter=',')
X_train, y_train = data[:, :4], data[:, 4]

initial_w, initial_b = np.zeros(X_train.shape[1]), 0

X_train = z_score_normalization(X_train)

linear_regression = LinearRegression()

final_w, final_b, _, _ = linear_regression.train(
    x=X_train,
    y=y_train,
    w_init=initial_w,
    b_init=initial_b,
    alpha=1.0e-1,
    iterations=1000,
    lambda_=0,
)

print(f"final_w: {final_w}, final_b: {final_b}")

yhat = linear_regression.predict(x=X_train, w=final_w, b=final_b)

print(f"yhat: {np.round(yhat[:5])}")
print(f"ytrain: {np.round(y_train[:5])}")
