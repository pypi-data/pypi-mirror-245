import numpy as np
from nptyping import NDArray, Int, Shape
from typing import Any


# TODO test
def normalize(points=NDArray[Shape["*, *"], Any], ranges=None):
    if ranges is None:
        ranges = np.array([np.min(points, axis=0), np.max(points, axis=0)])
    return (points - ranges[:, 0]) / (ranges[:, 1] - ranges[:, 0])
