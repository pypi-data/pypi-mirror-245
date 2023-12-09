from scioptim.test_objectives.base import TestObjective
from scipy.stats import multivariate_normal
from typing import List, Union
from scioptim import VarType
import numpy as np


class SphereFunction(TestObjective):
    DIRECTION = "min"
    UPPER_THRESHOLD = 1e-4

    def __init__(self, **kwargs):
        input_dim = self.input_dim_from_kwargs(**kwargs)
        if input_dim is None:
            input_dim = 2

        if "input_ranges" not in kwargs:
            kwargs["input_ranges"] = [[-10, 10]] * input_dim

        kwargs["input_dim"] = input_dim
        kwargs["input_types"] = [VarType.CONTINUOUS] * input_dim

        super().__init__(**kwargs)

    def evaluate(self, x) -> np.ndarray:
        y = np.sum(x**2, axis=1)
        return y

    def get_target(self) -> np.ndarray:
        return np.array([0])

    def get_optimum(self) -> np.ndarray:
        return np.zeros(self.output_dim)


class SphereFunction_1D(SphereFunction):
    def __init__(self, **kwargs):
        super().__init__(input_dim=1, **kwargs)


class SphereFunction_3D(SphereFunction):
    def __init__(self, **kwargs):
        super().__init__(input_dim=3, **kwargs)


class SphereFunction_5D(SphereFunction):
    def __init__(self, **kwargs):
        super().__init__(input_dim=5, **kwargs)


class SphereFunction_10D(SphereFunction):
    def __init__(self, **kwargs):
        super().__init__(input_dim=10, **kwargs)
