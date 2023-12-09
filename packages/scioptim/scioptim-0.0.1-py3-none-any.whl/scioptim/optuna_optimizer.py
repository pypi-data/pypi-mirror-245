import optuna
from typing import Type
from scioptim import Optimizer, VarType
import numpy as np


class OptunaOptimizer(Optimizer):
    SAMPLER: Type[
        optuna.samplers.BaseSampler
    ] = None  # optuna sampler used in the optimizer

    def __init__(self, *args, sampler_kwargs=None, **kwargs):
        """
        Initialize the OptunaOptimizer instance.

        Args:
            *args: Variable length argument list.
            sampler_kwargs (dict, optional): Keyword arguments for the sampler.
            **kwargs: Arbitrary keyword arguments.
        """
        if sampler_kwargs is None:
            sampler_kwargs = {}
        self._sampler_kwargs = sampler_kwargs
        super().__init__(*args, **kwargs)
        self._sampler_kwargs["seed"] = self.seed

    def _get_trial_generator(self, idx):
        """
        Generates the variable sampler used in Optuna trials.

        Args:
            idx (int): Index of the variable in input_types.

        Returns:
            Callable: A function that returns a suggestion from the trial.
        """
        vtype = self.input_types[idx]
        if vtype == VarType.INTEGER:
            return lambda trial: trial.suggest_int(
                self.input_names[idx],
                *self.input_ranges[idx],
                step=self.input_resolution[idx],
            )
        elif vtype == VarType.CONTINUOUS:
            return lambda trial: trial.suggest_float(
                self.input_names[idx],
                *self.input_ranges[idx],
                step=self.input_resolution[idx],
            )
        elif vtype == VarType.CATEGORICAL:
            return lambda trial: trial.suggest_categorical(
                self.input_names[idx], self.input_ranges[idx]
            )

    def reset(self):
        """
        Resets the optimizer state, creating a new Optuna study with a specified sampler.
        """
        prelev = optuna.logging.get_verbosity()
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        sampler = self.SAMPLER(
            **{**self._sampler_kwargs, "seed": self.rnd_gen.randint(1e9)}
        )  # Make the sampler behave in a deterministic way.
        self._study = optuna.create_study(sampler=sampler, direction="minimize")
        self._ask_parameters = [
            self._get_trial_generator(i) for i in range(self.input_dim)
        ]
        self._open_trials = []

        optuna.logging.set_verbosity(prelev)

        # initial sampling to create distributions
        self.sample(1)

    def fit(self, data: np.ndarray, append: bool = True):
        """
        Fit the optimizer with provided data.

        Args:
            data (np.ndarray): Data array containing single points in parameter space, including outcomes.
            append (bool): Whether to append the new data to existing data or replace it.
        """
        super().fit(data, append=append)
        input_names = self.input_names
        if len(data) == 0:
            return

        for point in data:
            val = self._get_optimization_value(point)
            reported = self._update_or_add_trial(input_names, point, val)
            if not reported:
                self._add_new_trial(input_names, point, val)

    def _get_optimization_value(self, point: np.ndarray) -> float:
        """
        Converts the outcome of a point to a value for optimization.

        Args:
            point (np.ndarray): A single data point.

        Returns:
            float: The value used for optimization.
        """
        if self.direction == "max":
            return -point[-1]
        elif self.direction == "min":
            return point[-1]
        else:
            return np.abs(point[-1] - self.direction)

    def _update_or_add_trial(self, input_names, point, val) -> bool:
        """
        Updates an existing trial or flags the need to add a new trial.

        Args:
            input_names (List[str]): Names of input variables.
            point (np.ndarray): A single data point.
            val (float): The optimization value for the trial.

        Returns:
            bool: True if the trial was updated, False otherwise.
        """
        for t in self._open_trials:
            if all([v == t.params[input_names[j]] for j, v in enumerate(point[:-1])]):
                self._study.tell(t, val)
                self._open_trials.remove(t)
                return True
        return False

    def _add_new_trial(self, input_names, point, val):
        """
        Adds a new trial to the Optuna study.

        Args:
            input_names (List[str]): Names of input variables.
            point (np.ndarray): A single data point.
            val (float): The optimization value for the trial.
        """
        trial = optuna.trial.create_trial(
            params={input_names[j]: v for j, v in enumerate(point[:-1])},
            distributions=self._distribuions,
            values=[val],
        )
        self._study.add_trial(trial)

    def sample(self, n: int) -> np.ndarray:
        """
        Sample new points using the Optuna study.

        Args:
            n (int): Number of new points to sample.

        Returns:
            np.ndarray: Sampled points.
        """
        sample_datapoints = np.zeros((n, self.input_dim))
        for i in range(n):
            trial = self._study.ask()
            for j, v in enumerate(self._ask_parameters):
                sample_datapoints[i, j] = v(trial)
            self._distribuions = trial.distributions
            self._open_trials.append(trial)
        return sample_datapoints


class RandomSamplerOptimizer(OptunaOptimizer):
    """
    Optimizer that utilizes Optuna's Random Sampler.

    This optimizer is based on the Optuna framework and employs a random sampling strategy
    to generate trial parameters. It's suitable for scenarios where a random search approach
    is preferred over more structured sampling methods.
    """

    SAMPLER = optuna.samplers.RandomSampler


class TPEOptimizer(OptunaOptimizer):
    """
    Optimizer that utilizes Optuna's Tree-structured Parzen Estimator (TPE) Sampler.

    TPE is a Bayesian optimization approach. This optimizer is useful for scenarios
    where an informed search based on previous trials is desired. It can be particularly
    effective in high-dimensional spaces.

    Args:
        *args: Variable length argument list.
        multivariate (bool): Indicates whether the sampler should sample multiple
                             parameters simultaneously rather than one at a time.
        **kwargs: Arbitrary keyword arguments.
    """

    SAMPLER = optuna.samplers.TPESampler

    def __init__(self, *args, multivariate=True, **kwargs):
        sampler_kwargs = kwargs.pop("sampler_kwargs", {})
        sampler_kwargs["multivariate"] = multivariate
        super().__init__(*args, sampler_kwargs=sampler_kwargs, **kwargs)


class CmaEsOptimizer(OptunaOptimizer):
    """
    Optimizer that utilizes Optuna's CMA-ES (Covariance Matrix Adaptation Evolution Strategy) Sampler.

    CMA-ES is an evolutionary algorithm for difficult non-linear non-convex black-box
    optimization problems. It is well-suited for continuous domains and particularly
    effective in scenarios where the parameter space is large and the underlying objective
    function is complex and involves many local optima.
    """

    SAMPLER = optuna.samplers.CmaEsSampler
