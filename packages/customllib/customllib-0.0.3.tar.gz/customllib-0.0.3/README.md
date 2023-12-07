# Customllib

A custom machine learning library.

## Install

```shell
pip install customllib
```

## Usage

See the [full example](examples%2Fhouse_prices_prediction.py) at the examples directory

```python
import numpy as np
from customllib.supervised.regression.linear_regression import LinearRegression

# Load our data set
X_train = np.array([1.0, 2.0])
y_train = np.array([300.0, 500.0])

# Train the model
linear_regression = LinearRegression()
final_w, final_b, _, _ = linear_regression.train(
    x=X_train,
    y=y_train,
    w_init=0,
    b_init=0,
    alpha=1.0e-1,
    iterations=1000,
    lambda_=0,
)

# Predict
yhat = linear_regression.predict(x=X_train, w=final_w, b=final_b)

# Result
print(f"yhat: {yhat}")
print(f"ytrain: {y_train}")
```

## Examples

See [README.md](examples%2FREADME.md) of the examples' directory.

## License

[MIT License](LICENSE)
