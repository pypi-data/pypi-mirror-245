from dataclasses import dataclass
import numpy as np
from scipy.stats import pearsonr

from .linalg import Vector, Matrix, Ones


@dataclass(frozen=True)
class LinearRegressionResult:
    """
        This class is the output of the LinearRegressor.fit method.

        The parameters are:
            m: float, angular coefficient.
            b: float, y-axis interception.
            rho: scipy.stats.PearsonResult.
            mse: float, mean-squared error of the ground-truth and the predicted values.
        
        The model is simple:
            $\tilde{y} = mx + b$
    """

    m: float
    b: float
    rho: float
    mse: float


class LinearRegressor:
    def __init__(self):
        pass

    def fit(self, x, y):
        N = len(x)
        ones = Ones(size=N)

        x_ = np.hstack([x, ones])
        o = np.linalg.inv(x_.T @ x_) @ x_.T @ y
        m = o[0][0]
        b = o[1][0]

        y_ = m * x + b

        rho = pearsonr(y.reshape(-1), y_.reshape(-1))

        mse = np.linalg.norm(y - y_, axis=0).mean()

        result = LinearRegressionResult(
            m=m,
            b=b,
            rho=rho,
            mse=mse
        )

        return result