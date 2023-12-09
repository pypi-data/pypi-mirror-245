from calendar import c
from statistics import median
from typing import List, Union
from scioptim.base import VarType, Model, RandomStateMixin
import numpy as np


# base class for virtual problem generators
class TestObjective(RandomStateMixin, Model):
    DIRECTION = "max"
    DEFAULT_TRIES = 1e5

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._median = None
        self._point_evaluator = None

    def get_optimum(self) -> np.ndarray:
        # returns the optimal input parameters as an array with shape (N,input_dim) where N is the number of optimal points (mostly 1)
        raise NotImplementedError("get_target not implemented")

    def get_target(self) -> np.ndarray:
        # returns the optimal output values as an array with shape (output_dim)
        raise NotImplementedError("get_target not implemented")

    def get_median(self):
        # returns the median of the output values as an array with shape (output_dim)
        if self._median is None:
            d = self.get_grid_points(
                grid_shape=False, resolution=int(np.ceil(10000 ** (1 / self.input_dim)))
            )
            self._median = np.median(d[:, -self.output_dim :], axis=0)
        return self._median

    # provides a way to compare the performance of different optimizer by implementing a point system to each test objective
    # by default it scores using a gauss distribution with mean at the optimum and a std, such that the median of the output values is 0.1
    # the score is then clipped between 0 and 1
    def point_y(
        self, y, reduction="mean", sigfac=10 * (np.sqrt(2 * np.log(2)))
    ) -> np.ndarray:
        # sigfac how many sigmas the median should be away from the optimum, default ~ 2.355 to give a median point of 0.5

        if self._point_evaluator is None:
            med = self.get_median()
            target = self.get_target()

            sig = np.abs(target - med) / sigfac
            d = 2 * np.power(sig, 2.0)

            def point_evaluator(x):
                return np.exp(-np.power(x - target, 2.0) / d)

            self._point_evaluator = point_evaluator

        p = np.clip(self._point_evaluator(y), 0.0, 1.0)
        if reduction == "mean":
            return p.mean(axis=1)
        elif reduction == "max":
            return p.max(axis=1)
        elif reduction == "min":
            return p.min(axis=1)
        elif reduction == "median":
            return np.median(p, axis=1)
        elif reduction == "none" or reduction is None:
            return p
        elif reduction == "sum":
            return p.sum(axis=1)
        else:
            raise ValueError(f"unknown reduction method '{reduction}'")
