from typing import List, Callable
from scioptim import Optimizer, Model
import numpy as np
from scipy.optimize import minimize
from scipy.stats import gaussian_kde
import sympy as sp
from scioptim import VarType

# input x1 x2 x3
# y= a*x1**0*x2**0*x3**0 + b x1**1*x2**0*x3**0 + c

# Define a constant for the default additional input dimension
DEFAULT_TO_INPUT_DIM = 1


class FunctionOptimizer(Model, Optimizer):
    def __init__(
        self,
        function: Callable[[np.ndarray, np.ndarray], np.ndarray],
        parameters: List[str],
        parameter_initials: List[float] = None,
        *args,
        sample_k: int = 5,
        **kwargs,
    ):
        self._function = function
        self._parameters = parameters

        if parameter_initials is not None:
            if not len(parameter_initials) == len(parameters):
                raise ValueError(
                    f"Wrong number of initial parameters. Expected {len(parameters)}, got {len(parameter_initials)}"
                )
            self._parameter_initials = np.array(parameter_initials)
        else:
            self._parameter_initials = None

        self._sample_k = max(1, int(sample_k))
        super().__init__(*args, **kwargs)

    def reset(self):
        if self._parameter_initials is None:
            self._covars = self.rnd_gen.rand(len(self._parameters))
        else:
            self._covars = self._parameter_initials.copy()

        # wrap function to accept covars as last argument
        def f(xdata, *covars):
            covars = np.array(covars)
            res = self._function(xdata, covars)
            res = res.reshape(xdata.shape[0], -1)
            return res

        # Define the sampler function
        def s(xdata):
            return f(xdata, *self._covars)

        self._fitter = f
        self._sampler = s

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """
        Evaluate the polynomial model on input points.

        Args:
            x (np.ndarray): Input points for evaluation.

        Returns:
            np.ndarray: Evaluated results.
        """
        x = np.array(x)
        x = x.reshape(-1, self.input_dim)
        return self._sampler(x)

    def _sort_samples(self, sample_datapoints: np.ndarray) -> np.ndarray:
        """
        Sorts the sampled data points based on the specified direction.

        Args:
            sample_datapoints (np.ndarray): Sampled data points.

        Returns:
            np.ndarray: Sorted sampled data points.
        """
        if self.direction == "max":
            return sample_datapoints[np.argsort(sample_datapoints[..., -1])[::-1]]
        elif self.direction == "min":
            return sample_datapoints[np.argsort(sample_datapoints[..., -1])]
        else:
            return sample_datapoints[
                np.argsort(np.abs(sample_datapoints[..., -1] - self.direction))
            ]

    def _add_additional_points(
        self, sample_datapoints: np.ndarray, n: int
    ) -> np.ndarray:
        """
        Adds additional points to the sampled data if available.

        Args:
            sample_datapoints (np.ndarray): Sampled data points.
            n (int): Number of points to return.

        Returns:
            np.ndarray: Sampled data points with additional points added, if available.
        """
        gp = self.get_grid_points(resolution=2, evaluated=False, grid_shape=False)
        _dp = gp[
            ~np.array([np.equal(a, self.datapoints[:, :-1]).all(1).any() for a in gp])
        ]
        sample_datapoints = sample_datapoints[:, :-1]
        if len(_dp) > 0:
            sample_datapoints = np.concatenate((_dp, sample_datapoints), axis=0)
        return sample_datapoints[:n]

    def sample(self, n: int, exploitation: float = 0.1):
        """
        Sample new points using the polynomial model.

        Args:
            n (int): Number of new points to sample.

        Returns:
            np.ndarray: Sampled points.
        """
        exploitation = min(max(exploitation, 0), 1)
        k = self._sample_k
        sample_datapoints = np.zeros((n * k, self.input_dim + self.output_dim))
        ipranges = self.input_ranges
        ub, lb = ipranges[:, 1].astype(float), ipranges[:, 0].astype(float)

        # Sample points uniformly within the specified range for each dimension
        for i in range(self.input_dim):
            sample_datapoints[:, i] = self.rnd_gen.rand(n * k) * (ub[i] - lb[i]) + lb[i]

        sample_datapoints[:, -self.output_dim :] = self._sampler(
            sample_datapoints[:, :-1]
        )

        mask = np.zeros(sample_datapoints.shape[0], dtype=bool)
        # Randomly choose m indices to set to True
        mask[
            np.random.choice(n, max(1, int(n * (1 - exploitation))), replace=False)
        ] = True
        rand_samples = sample_datapoints[mask]
        other_samples = sample_datapoints[~mask]
        # Sort sampled points based on direction
        sample_datapoints = np.concatenate(
            (rand_samples, self._sort_samples(other_samples))
        )
        # Add additional points if available
        return self._add_additional_points(sample_datapoints, n)

    def fit(self, data: np.ndarray, append: bool = True):
        """
        Fit the polynomial model to provided data.

        Args:
            data (np.ndarray): Data array containing points in parameter space, including outcomes.
            append (bool): Whether to append the new data to existing data or replace it.
        """
        data = np.array(data).astype(float)  # Ensure data is of type float
        super().fit(data, append=append)

        # Fit the model only if sufficient data is available
        if len(data) > 0 and len(self.datapoints) >= len(self._covars):
            self._fit_model()

    def _gen_min(self, xdata: np.ndarray, ydata: np.ndarray):
        """
        Generates a function to minimize, used in fitting the polynomial model to data.

        This method creates an error function that quantifies the difference between
        the observed data and the model's predictions. It employs a Gaussian Kernel
        Density Estimation (KDE) to apply weights to the error based on the density
        of the data points, giving more importance to regions with more data.

        The error function is designed for use with a numerical optimization algorithm
        (e.g., scipy.optimize.minimize) to find the optimal polynomial coefficients
        that minimize this weighted error.

        Args:
            xdata (np.ndarray): Input data points.
            ydata (np.ndarray): Output data points.

        Returns:
            Callable: The function to minimize.
        """
        # Estimate density using a Gaussian kernel
        w = gaussian_kde(xdata.T)(xdata.T).reshape(xdata.shape[0], 1)

        # Define the error function to minimize
        def f(covars):
            err = np.mean(((ydata - self._fitter(xdata, *covars)) / w) ** 2)
            return err

        return f

    def _fit_model(self):
        """
        Perform the model fitting using nonlinear optimization.
        """
        dp = self.datapoints
        res = minimize(
            self._gen_min(dp[:, : -self.output_dim], dp[:, -self.output_dim :]),
            x0=self._covars,
            options=dict(maxiter=100),
        )
        self._covars = res.x


def _placeholderfunction(*args, **kwargs):
    raise NotImplementedError("still using placeholder function")


class NPolynomialOptimizer(FunctionOptimizer):
    """
    Optimizer that fits an N-dimensional polynomial function to data.

    This optimizer is designed to fit a polynomial model to the provided data points.
    It uses nonlinear optimization techniques to find the polynomial coefficients that
    best fit the data according to the specified objective direction.

    Args:
        *args: Variable length argument list.
        p (int, optional): The degree of the polynomial. If None, it defaults to input_dim + 1.
        sample_k (int): The factor by which to multiply the number of samples generated.
        **kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, *args, p: int = None, **kwargs):
        """
        Initialize the NPolynomialOptimizer instance.
        """
        self._p = p
        kwargs["output_dim"] = kwargs.get("output_dim", 1)
        f = _placeholderfunction
        super().__init__(function=f, parameters=[], *args, **kwargs)
        self._regenerate_function()

    def _regenerate_function(self):
        if self._p is None:
            self._p = self.input_dim + DEFAULT_TO_INPUT_DIM

        terms = np.unique(
            np.array(
                np.meshgrid(*[np.arange(self._p + 1) for _ in range(self.input_dim)])
            ).T.reshape(-1, self.input_dim),
            axis=0,
        )
        termssum = np.sum(terms, axis=1)
        terms = terms[termssum <= self._p]

        _t_range = np.arange(terms.shape[0])
        self._parameters = [f"a{i+1}" for i in range(terms.shape[0])]

        def _func(xdata, covars):
            o = np.zeros((xdata.shape[0], self.output_dim))
            for i in range(xdata.shape[0]):
                for j in _t_range:
                    o[i] += covars[j] * np.prod(xdata[i] ** terms[j])
            return o

        self._function = _func


class StringFunctionOptimizer(FunctionOptimizer):
    def __init__(self, funcstring: str, *args, **kwargs):
        # generate parameters from function string
        self._funcstring = funcstring
        self._expression = sp.sympify(funcstring)
        symbols = [str(s) for s in self._expression.free_symbols]
        xsymbols = list(sorted(s for s in symbols if s.startswith("x")))
        covarnames = [s for s in symbols if s not in xsymbols]
        # self._covars = np.random.rand(len(self.covarnames))  # Initialize coefficients to zeros

        compiled_func = np.vectorize(
            sp.lambdify(
                tuple(xsymbols + covarnames),
                self._expression,
                modules=[{"np": np, "sp": sp}],
            )
        )

        def _function(xdata: np.ndarray, covars: np.ndarray):
            covars = np.tile(covars, xdata.shape[0]).reshape(xdata.shape[0], -1)
            return compiled_func(*np.concatenate((xdata, covars), axis=1).T)

        kwargs["input_names"] = kwargs.get("input_names", xsymbols)
        kwargs["input_types"] = kwargs.get(
            "input_types", [VarType.CONTINUOUS] * len(kwargs["input_names"])
        )
        kwargs["input_ranges"] = kwargs.get(
            "input_ranges", [[-1e32, 1e32]] * len(kwargs["input_names"])
        )

        super().__init__(
            function=_function,
            parameters=covarnames,
            *args,
            **kwargs,
        )
