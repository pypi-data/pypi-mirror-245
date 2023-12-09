from scioptim.test_objectives.base import TestObjective
from scipy.stats import multivariate_normal
from typing import List, Union
from scioptim import VarType
import numpy as np
from scipy.optimize import minimize


# generates an multi max gauss prblem
class multi_max_gauss(TestObjective):
    DIRECTION = "max"
    LOWER_THRESHOLD = 1 - 1e-2
    # DEFAULT_TRIES= 150

    def __init__(
        self,
        input_dim=1,
        input_ranges=None,
        maxima=2,
        weights=None,
        mean=None,
        cov=None,
        input_types=None,
        **kwargs,
    ):
        if input_types is None:
            input_types = [VarType.CONTINUOUS] * input_dim
        super().__init__(
            input_dim=input_dim,
            input_types=input_types,
            input_ranges=[[0, 1]] * input_dim if input_ranges is None else input_ranges,
            **kwargs,
        )

        if mean is None:
            mean = np.array([self.rnd_gen.rand(input_dim) * 10 for i in range(maxima)])
        else:
            mean = np.array(mean)
        if weights is None:
            weights = self.rnd_gen.rand(maxima)

        weights = np.array(weights) / np.max(weights)

        if cov is None:
            if input_dim == 1:
                cov = np.array([[[1]] for i in range(maxima)])
            else:
                cov = np.array([np.diag(np.ones(input_dim)) for i in range(maxima)])
        else:
            cov = np.array(cov)
            if cov.ndim == 1:
                cov = cov[None, :]

            if cov.ndim == 2:
                cov = np.tile(cov, (maxima, 1, 1))

        assert (
            weights.ndim == 1
        ), f"weights must have shape ({maxima}) but is {weights.shape}"
        assert (
            weights.shape[0] == maxima
        ), f"weights must have shape ({maxima}) but is {weights.shape}"

        assert (
            mean.ndim == 2
        ), f"mean must have shape ({maxima},{input_dim}) but is {mean.shape}"
        assert (
            mean.shape[0] == maxima
        ), f"mean must have shape ({maxima},{input_dim}) not {mean.shape}"
        assert (
            mean.shape[1] == input_dim
        ), f"mean must have shape {input_dim} not {mean.shape}"

        assert (
            cov.ndim == 3
        ), f"cov must have shape ({maxima},{input_dim},{input_dim}) but is {cov.shape}"
        assert (
            cov.shape[0] == maxima
        ), f"cov must have shape ({maxima},{input_dim},{input_dim}) not {cov.shape}"
        assert (
            cov.shape[1] == input_dim
        ), f"cov must have shape ({maxima},{input_dim},{input_dim}) not {cov.shape}"
        assert (
            cov.shape[2] == input_dim
        ), f"cov must have shape ({maxima},{input_dim},{input_dim}) not {cov.shape}"

        self._vars = [
            multivariate_normal(mean=mean[i], cov=cov[i]) for i in range(maxima)
        ]
        self._div = np.array(
            [(self._vars[i].pdf([mean[i]]) / weights[i]) for i in range(maxima)]
        )

        if input_ranges is None:
            input_ranges = np.ones((input_dim, 2))
            for d in range(input_dim):
                input_ranges[d] *= mean[0, d]
            for mx in range(maxima):
                s = 1
                m = mean[mx]
                c = cov[mx]
                p1 = np.array([m + c[d, d] * s for d in range(input_dim)])

                d1 = self(p1)
                while np.any(d1 > 0.005):
                    s += 1
                    p1 = np.array([m + c[d, d] * s for d in range(input_dim)])
                    d1 = self(p1)
                p2 = np.array([m - c[d, d] * s for d in range(input_dim)])
                d2 = self(p2)

                for d in range(input_dim):
                    input_ranges[d, 0] = np.minimum(input_ranges[d, 0], p2[0, d])
                    input_ranges[d, 1] = np.maximum(input_ranges[d, 1], p1[0, d])

            self._input_ranges = input_ranges

        def _min(x):
            return -self.evaluate(x)

        res = minimize(
            _min,
            x0=mean[np.argmax(weights)],
            bounds=self._input_ranges,
        )
        self._opt = res.x.flatten()[None, :]
        self._div *= self(self._opt).flatten()[0]

    def evaluate(self, x) -> np.ndarray:
        y = self._vars[0].pdf(x) / self._div[0]
        for i, _v in enumerate(self._vars[1:]):
            y += _v.pdf(x) / self._div[i + 1]
        return y

    def get_target(self):
        return np.array([1])

    def get_optimum(self) -> np.ndarray:
        return self._opt


class single_max_1d_gauss(multi_max_gauss):
    DEFAULT_TRIES = 100

    def __init__(self, **kwargs):
        kwargs["maxima"] = 1
        kwargs["input_dim"] = 1
        super().__init__(**kwargs)


class single_max_2d_gauss(multi_max_gauss):
    DEFAULT_TRIES = 100

    def __init__(self, **kwargs):
        kwargs["maxima"] = 1
        kwargs["input_dim"] = 2
        super().__init__(**kwargs)


class single_max_3d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 1
        kwargs["input_dim"] = 3
        super().__init__(**kwargs)


class single_max_5d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 1
        kwargs["input_dim"] = 5
        super().__init__(**kwargs)


class single_max_10d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 1
        kwargs["input_dim"] = 10
        super().__init__(**kwargs)


class double_max_1d_gauss(multi_max_gauss):
    DEFAULT_TRIES = 100

    def __init__(self, **kwargs):
        kwargs["maxima"] = 2
        kwargs["input_dim"] = 1
        super().__init__(**kwargs)


class double_max_2d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 2
        kwargs["input_dim"] = 2
        super().__init__(**kwargs)


class double_max_3d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 2
        kwargs["input_dim"] = 3
        super().__init__(**kwargs)


class double_max_5d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 2
        kwargs["input_dim"] = 5
        super().__init__(**kwargs)


class double_max_10d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 2
        kwargs["input_dim"] = 10
        super().__init__(**kwargs)


class triple_max_1d_gauss(multi_max_gauss):
    DEFAULT_TRIES = 100

    def __init__(self, **kwargs):
        kwargs["maxima"] = 3
        kwargs["input_dim"] = 1
        super().__init__(**kwargs)


class triple_max_2d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 3
        kwargs["input_dim"] = 2
        super().__init__(**kwargs)


class triple_max_3d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 3
        kwargs["input_dim"] = 3
        super().__init__(**kwargs)


class triple_max_5d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 3
        kwargs["input_dim"] = 5
        super().__init__(**kwargs)


class triple_max_10d_gauss(multi_max_gauss):
    def __init__(self, **kwargs):
        kwargs["maxima"] = 3
        kwargs["input_dim"] = 10
        super().__init__(**kwargs)
