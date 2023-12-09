from __future__ import annotations
from typing import List
import torch
from botorch.models import SingleTaskGP
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood

import botorch

from botorch.acquisition.acquisition import AcquisitionFunction
from botorch.acquisition import (
    qExpectedImprovement,
    qUpperConfidenceBound,
    qProbabilityOfImprovement,
    qSimpleRegret,
)
from botorch.optim import optimize_acqf
from botorch.sampling import SobolQMCNormalSampler
from botorch.utils.transforms import normalize, unnormalize
import numpy as np

from scioptim.base import (
    Optimizer,
    Model,
    DuplicatePointHandler,
    IgnoreDuplicatePointHandler,
    RandomPointDuplicatePointHandler,
)

## Assumptions/settings:
# input = normalized
# output = unnormalized (optional for later: standardization)


class BayesionDefaultDuplicatePointHandler(DuplicatePointHandler):
    def handle_duplicate_points(
        self,
        optimizer: BayesianOptimizer,
        all_points: np.ndarray,
        duplicate_indices: List[int],
    ) -> np.ndarray:
        """
        Handle duplicate points in a Bayesian optimization context by generating and using various acquisition functions.

        Args:
            optimizer (Optimizer): The optimizer instance.
            all_points (np.ndarray): Array of all points in the current optimization process.
            duplicate_indices (List[int]): Indices of the duplicate points in `all_points`.

        Returns:
            np.ndarray: New set of points with duplicates handled, either through re-sampling or replacement with random points.
        """

        def _gen_aq():
            sampler = SobolQMCNormalSampler(  # Standard sampler only called for specifying seed
                sample_shape=torch.Size([1024]),
                seed=optimizer.seed,
            )

            aquisition_function = qSimpleRegret(optimizer._dir_single_model, sampler)
            yield aquisition_function

            if optimizer.direction == "max":
                best = optimizer.datapoints[:, -1].max()
            elif optimizer.direction == "min":
                best = -optimizer.datapoints[:, -1].min()
            else:
                # towards point
                dp = optimizer.datapoints[:, -1]
                best = -dp[np.abs(dp - optimizer.direction).argmin()]

            aquisition_function = qExpectedImprovement(
                optimizer._dir_single_model,
                best_f=best,
                sampler=sampler,
            )
            yield aquisition_function

            aquisition_function = qUpperConfidenceBound(
                optimizer._dir_single_model, beta=0.1, sampler=sampler
            )
            yield aquisition_function

            aquisition_function = qProbabilityOfImprovement(
                optimizer._dir_single_model,
                best_f=best,
                sampler=sampler,
            )
            yield aquisition_function

            aquisition_function = qSimpleRegret(optimizer._dir_single_model, sampler)
            yield aquisition_function

        o_duplicate_point_sampled = optimizer.duplicate_point_sampled
        optimizer.duplicate_point_sampled = IgnoreDuplicatePointHandler()

        n = len(duplicate_indices)
        for aq in _gen_aq():
            new_points = optimizer.sample(len(duplicate_indices), aq)
            new_points = optimizer.map_points_to_resolution(new_points, unique=True)
            all_points[duplicate_indices[: len(new_points)]] = new_points
            duplicate_indices = optimizer.get_duplicate_points_index(
                all_points,
            )
            if len(duplicate_indices) == 0:
                break

        nall = len(all_points)

        if len(duplicate_indices) > 0:
            handler = RandomPointDuplicatePointHandler()
            all_points = handler(
                optimizer, all_points, duplicate_indices=duplicate_indices
            )

        optimizer.duplicate_point_sampled = o_duplicate_point_sampled
        duplicate_indices = optimizer.get_duplicate_points_index(
            all_points,
        )
        return all_points


class BayesianOptimizer(Optimizer, Model):
    """
    A Bayesian Optimizer that integrates Gaussian process models for optimization tasks.

    This optimizer extends the general Optimizer and Model classes, specializing in Bayesian optimization techniques.
    It utilizes Gaussian process models (SingleTaskGP) from BoTorch, handling both the optimization process and the
    model fitting with Bayesian principles.

    Attributes:
        DEFAULT_DUPLICATE_POINT_HANDLER (DuplicatePointHandler): The default handler for duplicate points in the
        optimization process, set to BayesionDefaultDuplicatePointHandler.

    Methods:
        __init__(*args, **kwargs): Initializes the BayesianOptimizer with default settings for
        input and output normalization.
        reset(): Resets the internal Gaussian process models and all the data points.
        sample(n, aquisition_function=None): Samples new points using a specified or default acquisition function.
        eval(x): Evaluates the Gaussian process model on given input data, returning predictions.
        evaluate(x, with_std=False): Wrapper for 'eval' with optional standard deviation inclusion in the output.
        fit(data, append=True): Fits the optimizer with new data, updating the Gaussian process models.

    Example:
        >>> optimizer = BayesianOptimizer()
        >>> optimizer.fit(data)
        >>> new_points = optimizer.sample(5)
        >>> predictions = optimizer.evaluate(new_points)
    """

    DEFAULT_DUPLICATE_POINT_HANDLER = BayesionDefaultDuplicatePointHandler

    def __init__(self, *args, **kwargs):
        """
        Initialize the BayesianOptimizer, setting up default bounds for input and output data normalization.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self._single_model: SingleTaskGP = None
        self._dir_single_model: SingleTaskGP = None
        super().__init__(*args, **kwargs)
        self._standard_x_bounds = torch.zeros((2, self.input_dim))
        self._standard_x_bounds[1] = 1.0
        self._standard_y_bounds = torch.zeros((2, self.output_dim))
        self._standard_y_bounds[1] = 1.0

    def reset(self):
        """
        Reset the internal models of the optimizer based on the current data points.
        This method initializes or re-initializes the Gaussian process models used in Bayesian optimization.
        """
        norm_data_x = torch.from_numpy(self.datapoints[:, : self.input_dim])
        norm_data_y = torch.from_numpy(self.datapoints[:, self.input_dim :])
        self._single_model = SingleTaskGP(norm_data_x, norm_data_y)
        self._dir_single_model = SingleTaskGP(norm_data_x, norm_data_y)

    def sample(self, n: int, aquisition_function: AcquisitionFunction = None):
        """
        Sample new points using the given acquisition function or a default one based on the optimizer's direction and data.

        Args:
            n (int): The number of new points to sample.
            aquisition_function (AcquisitionFunction, optional): A specific acquisition function to use. Defaults to None, in which case a default acquisition function based on optimization direction is used.

        Returns:
            np.ndarray: The sampled points after un-normalizing and converting categorical indices back to their original values.
        """
        sampler = (
            SobolQMCNormalSampler(  # Standard sampler only called for specifying seed
                sample_shape=torch.Size([1024]),
                seed=self.seed,
            )
        )
        if aquisition_function is None:
            if self.datapoints.shape[0] < 1:  # Case if LESS than 1 data point
                aquisition_function = qUpperConfidenceBound(
                    self._dir_single_model, beta=0.1, sampler=sampler
                )
            else:  # Case if MORE than 1 data point
                if self.direction == "max":
                    best = self.datapoints[:, -1].max()
                elif self.direction == "min":
                    best = -(self.datapoints[:, -1].min())
                else:
                    # towards point
                    dp = self.datapoints[:, -1]
                    best = -dp[np.abs(dp - self.direction).argmin()]

                aquisition_function = qExpectedImprovement(
                    self._dir_single_model,
                    best_f=best,
                    sampler=sampler,
                )
        with botorch.utils.sampling.manual_seed(seed=self.seed):
            initials = botorch.optim.initializers.gen_batch_initial_conditions(
                aquisition_function,
                bounds=self._standard_x_bounds,
                q=n,
                num_restarts=10,
                raw_samples=128,
            )
        standart_candidates, acq_value = optimize_acqf(
            aquisition_function,
            bounds=self._standard_x_bounds,
            q=n,
            num_restarts=20,
            raw_samples=512,
            seed=self.seed,
            batch_initial_conditions=initials,
        )

        candidates = unnormalize(standart_candidates, bounds=self.input_ranges.T)
        # print("canidates",standart_candidates,candidates)
        candidates = candidates.detach().numpy()
        candidates = self.categorical_index_to_raw_if_needed(candidates)
        return candidates

    def eval(self, x):
        """
        Evaluate the Gaussian process model on unnormalized inputs.

        Args:
            x (np.ndarray): Input points for evaluation.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Means and standard deviations of the Gaussian process predictions.
        """
        norm_data_x = torch.from_numpy(x)
        norm_data_x = normalize(norm_data_x, bounds=self.input_ranges.T)
        std_can = self._single_model(norm_data_x)
        means = (std_can.loc.detach() * self.norm_std + self.norm_mean).numpy()
        std = (std_can.stddev.detach() * self.norm_std).numpy()
        return means, std

    def __call__(self, x, with_std=False, **kwargs):
        return super().__call__(x, with_std=with_std, **kwargs)

    def evaluate(self, x, with_std=False):
        """
        Evaluate the model with optional inclusion of standard deviations.

        Args:
            x (np.ndarray): Input points for evaluation.
            with_std (bool, optional): Flag to indicate whether to return standard deviations along with means. Defaults to False.

        Returns:
            Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]: Evaluated means, and optionally standard deviations.
        """
        means, std = self.eval(x)
        if with_std:
            return means, std
        return means

    def fit(self, data, append=True):
        """
        Fit the optimizer with data, normalizing input and optionally output, and updating the Gaussian process models.

        Args:
            data (np.ndarray): Data array containing single points in parameter space including outcomes. The shape of the array must be (n_samples, input_dim + output_dim).
            append (bool, optional): Whether to append the new data to existing data or replace it. Defaults to True.
        """
        super().fit(data, append=append)

        norm_data_x = torch.from_numpy(self.intrinsic_datapoints[:, : self.input_dim])
        norm_data_y = torch.from_numpy(self.intrinsic_datapoints[:, self.input_dim :])
        # Normalization of input
        norm_data_x = normalize(norm_data_x, bounds=self.input_ranges.T)

        self.norm_mean = norm_data_y.mean(axis=0)
        self.norm_std = norm_data_y.std(axis=0)
        scaled_norm_data_y = (norm_data_y - self.norm_mean) / self.norm_std
        if self.direction == "max":
            dir_norm_data_y = scaled_norm_data_y
        elif self.direction == "min":  # change data to minimization problem
            dir_norm_data_y = -scaled_norm_data_y
        else:
            dir_norm_data_y = -np.abs(norm_data_y - self.direction)
            dir_norm_data_y = (
                dir_norm_data_y - dir_norm_data_y.mean(axis=0)
            ) / dir_norm_data_y.std(axis=0)

        # print(dir_norm_data_y)

        self._single_model = SingleTaskGP(norm_data_x, scaled_norm_data_y)
        mll = ExactMarginalLogLikelihood(
            self._single_model.likelihood, self._single_model
        )
        fit_gpytorch_mll(mll)

        if self.direction == "max":  # Maximization case
            self._dir_single_model = self._single_model
        else:  # NOT Maximization case
            self._dir_single_model = SingleTaskGP(norm_data_x, dir_norm_data_y)
            mll = ExactMarginalLogLikelihood(
                self._dir_single_model.likelihood, self._dir_single_model
            )
            fit_gpytorch_mll(mll)
