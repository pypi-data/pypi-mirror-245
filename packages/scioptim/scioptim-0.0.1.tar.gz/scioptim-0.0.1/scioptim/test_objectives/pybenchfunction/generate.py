from __future__ import annotations
from typing import Type, List, Optional
import scioptim
from scioptim.test_objectives.base import TestObjective
import numpy as np
import inspect
from .function import PyBenchFunction
from . import function

possible_dimensions = [1, 2, 3, 5, 10]
_INITIALIZED = False


def cls_dim_copm(cls: Type[PyBenchFunctionBase], d):
    if not issubclass(cls, PyBenchFunctionBase):
        raise TypeError("cls must be a subclass of PyBenchFunctionBase")

    if cls.testclass.is_dim_compatible(d):
        ins = cls(d)
        try:
            assert ins.get_optimum().shape[1] == d, f"Optimum must be {d}D"
            if ins.get_target() is not None:
                return True
        except AssertionError:
            return False
        except ValueError:
            return False
        except TypeError:
            return False
    return False


class PyBenchFunctionBase(TestObjective):
    DIRECTION = "min"
    testclass: Type[PyBenchFunction]

    def __init__(self, input_dim, *args, **kwargs):
        cls = self.testclass
        if cls is None:
            raise ValueError("PyBenchFunctionBase.testclass must be set")

        self._instance: PyBenchFunction = cls(d=input_dim)
        d = self._instance.dimensionality
        super().__init__(
            input_ranges=self._instance.input_domain,
            input_dim=d,
            input_types=[scioptim.VarType.CONTINUOUS] * d,
            output_dim=1,
        )

        self._veccall = np.vectorize(self._instance.__call__)

    def evaluate(self, X) -> np.ndarray:
        return np.apply_along_axis(self._instance.__call__, 1, X)

    def get_target(self) -> float:
        t = np.array(self._instance.get_global_minimum()[1])
        return t.min()  # only 1D output

    def get_optimum(self):
        op: np.ndarray = self._instance.get_global_minimum()[0]
        if op.ndim == 1:
            op = op.reshape(1, -1)
        if op.ndim != 2:
            raise ValueError("Optimum must be 2D")
        return op


def _generate_base_classes():
    def ClassFactory(cls: Type[PyBenchFunction]):
        name = f"{cls.__name__}"

        newclass = type(
            name,
            (PyBenchFunctionBase,),
            {
                "testclass": cls,
            },
        )
        return newclass

    _baseclasses: List[PyBenchFunctionBase] = []
    for name, obj in {
        _name: _obj
        for _name, _obj in vars(function).items()
        if (
            inspect.isclass(_obj)
            and issubclass(_obj, PyBenchFunction)
            and _obj != PyBenchFunction
        )
    }.items():  # create new dict since for some reason it changes during iteration
        _baseclasses.append(ClassFactory(obj))
    return _baseclasses
    # check if is subclass of BenchmarkFunction


def _generate_dimmed_classes(cls: Type[PyBenchFunctionBase]):
    _dimmed_classes = []

    def ClassFactory(cls: Type[PyBenchFunctionBase], dim):
        def __init__(self, *args, **kwargs):
            super(newclass, self).__init__(
                input_dim=dim,
                *args,
                **kwargs,
            )

        newclass: Type[PyBenchFunctionBase] = type(
            f"{cls.__name__}_{dim}d",
            (cls,),
            {
                "__init__": __init__,
            },
        )
        return newclass

    for d in possible_dimensions:
        if cls_dim_copm(cls, d):
            _dimmed_classes.append(ClassFactory(cls, d))
    return _dimmed_classes


if not _INITIALIZED:
    __all__ = []
    baseclasses: List[Type[PyBenchFunctionBase]] = []
    dimmed_classes: List[Type[PyBenchFunctionBase]] = []

    _baseclasses = _generate_base_classes()
    for c in _baseclasses:
        globals()[c.__name__] = c
        __all__.append(c.__name__)
        baseclasses.append(c)

    for c in _baseclasses:
        for dc in _generate_dimmed_classes(c):
            globals()[dc.__name__] = dc
            __all__.append(dc.__name__)
            dimmed_classes.append(dc)

__all__.extend(
    [
        "_INITIALIZED",
        "baseclasses",
        "dimmed_classes",
    ]
)
_INITIALIZED = True
