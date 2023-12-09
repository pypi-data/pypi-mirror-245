from __future__ import annotations
import numpy as np
from typing import List, Union, Any, Literal, Optional
from enum import Enum, unique


# Define variable types for optimization problems
@unique
class VarType(Enum):
    CONTINUOUS = 1
    INTEGER = 2
    CATEGORICAL = 3


# Default resolution for continuous variables
DEFAULT_RESOLUTION = 100


def input_types_from_kwargs(
    input_types: Optional[List[VarType]] = None,
    input_ranges: Optional[List[List[Union[int, float]]]] = None,
    input_dim: Optional[int] = None,
    input_names: Optional[List[str]] = None,
) -> List[VarType]:
    """
    Determine input types from keyword arguments.

    Args:
        input_types (Optional[List[VarType]]): List of input types.
        input_ranges (Optional[List[List[Union[int, float]]]]): List of input ranges.
        input_dim (Optional[int]): Dimensionality of the problem.

    Returns:
        List[VarType]: List of input types.
    """

    if input_types is not None:
        return input_types

    input_types = []
    if input_ranges is not None:
        for r in input_ranges:
            if len(r) != 2:
                input_types.append(VarType.CATEGORICAL)
            else:
                _sum = r[0] + r[1]
                if isinstance(_sum, int):
                    input_types.append(VarType.INTEGER)
                else:
                    input_types.append(VarType.CONTINUOUS)
        return input_types

    if input_dim is not None:
        return [VarType.CONTINUOUS] * input_dim

    if input_names is not None:
        return [VarType.CONTINUOUS] * len(input_names)

    raise ValueError("input_types, input_ranges, or input_dim must be specified")


def input_dim_from_kwargs(**kwargs):
    """
    Class method to determine input dimension from keyword arguments.
    Args:
        **kwargs: Variable keyword arguments.
    Returns:
        int: The determined input dimension, or None if not determinable.
    """
    input_dim = kwargs.get("input_dim")
    if input_dim is not None:
        return input_dim
    if kwargs.get("input_names") is not None:
        return len(kwargs.get("input_names"))
    if kwargs.get("input_types") is not None:
        return len(kwargs.get("input_types"))
    if kwargs.get("input_ranges") is not None:
        return len(kwargs.get("input_ranges"))

    raise ValueError(
        "input_dim must be specified if no other input information is given"
    )


class MissmatchDimensionException(Exception):
    pass


class ResolutionException(Exception):
    pass


class RangeException(Exception):
    pass


class CategoricalException(Exception):
    pass


class FixedVarBase:
    """
    Base class for objects containing parameter space.
    This class is used as a foundation for optimizers and models to define
    and handle their input and output parameters.
    """

    def __init__(
        self,
        input_ranges: List[List[Union[int, float]]],  # list of input ranges
        input_types: Optional[List[VarType]] = None,  # list of input types
        input_dim: Optional[int] = None,  # dimensionality of the problem
        input_names: Optional[List[str]] = None,  # list of input names
        input_resolution: Optional[
            List[Union[int, float]]
        ] = None,  # list of input resolutions TODO: use this
        output_names: Optional[List[str]] = None,  # list of output names
        output_dim: Optional[int] = 1,
    ):
        """
        Initialize the FixedVarBase object with input and output specifications.

        Args:
            input_types (List[VarType]): List of types for each input variable.
            input_ranges (List[List[Union[int, float]]]): List of ranges for each input variable.
            input_dim (int, optional): The dimensionality of the input space. Defaults to None.
            input_names (List[str], optional): Names of input variables. Defaults to None.
            input_resolution (List[Union[int, float]], optional): Resolution for each input variable. Defaults to None.
            output_names (List[str], optional): Names of output variables. Defaults to None.
            output_dim (int, optional): The dimensionality of the output space. Defaults to 1.
        """
        # Determine input dimension from arguments
        input_dim = input_dim_from_kwargs(
            input_dim=input_dim,
            input_names=input_names,
            input_types=input_types,
            input_ranges=input_ranges,
        )

        self._input_dim = input_dim
        self._output_dim = output_dim

        # Default input names if not provided
        if input_names is None:
            input_names = [f"x{i+1}" for i in range(input_dim)]

        # Default output names if not provided
        if output_names is None:
            output_names = [f"y{i+1}" for i in range(output_dim)]

        if input_types is None:
            input_types = input_types_from_kwargs(
                input_types=input_types,
                input_ranges=input_ranges,
                input_dim=input_dim,
            )
        # Validate and assign input types and ranges
        if len(input_types) != self.input_dim:
            raise MissmatchDimensionException(
                f"input_types must have length {self.input_dim} but has length {len(input_types)}"
            )
        self._input_types: List[VarType] = input_types

        if len(input_ranges) != self.input_dim:
            raise MissmatchDimensionException(
                f"input_ranges must have length {self.input_dim} but has length {len(input_ranges)}"
            )

        # Default input resolution for undefined resolutions
        if input_resolution is None:
            input_resolution = [None] * self.input_dim

        # Initialize categories for categorical variables
        self._categories = [None] * self.input_dim
        self._has_categorical = False
        for i in range(self.input_dim):
            if input_resolution[i] is None:
                # Default resolution for integer variables
                if input_types[i] == VarType.INTEGER:
                    input_resolution[i] = 1

            # Continuous variable validation
            if input_types[i] == VarType.CONTINUOUS:
                if input_resolution[i] is not None and input_resolution[i] <= 0:
                    raise ResolutionException(
                        f"input_resolution[{i}] must be None or >0 for continuous variable {input_names[i]}"
                    )
                if len(input_ranges[i]) != 2:
                    raise RangeException(
                        f"input_ranges[{i}] must have length 2 (min,max) for continuous variable {input_names[i]}"
                    )

                # resolution as difference to resolution as number of points
                if input_resolution[i] is not None:
                    input_resolution[i] = (
                        int(
                            (input_ranges[i][1] - input_ranges[i][0])
                            / input_resolution[i]
                        )
                        + 1
                    )

            # Integer variable validation
            if input_types[i] == VarType.INTEGER:
                if not isinstance(input_resolution[i], int):
                    raise ResolutionException(
                        f"input_resolution[{i}] must be an integer for integer variables {input_names[i]}"
                    )
                if input_resolution[i] <= 0:
                    raise ResolutionException(
                        f"input_resolution[{i}] must be greater than 0 for integer variables {input_names[i]}"
                    )
                if len(input_ranges[i]) != 2:
                    raise RangeException(
                        f"input_ranges[{i}] must have length 2 (min,max) for integer variable {input_names[i]}"
                    )

                # resolution as difference to resolution as number of points
                input_resolution[i] = (
                    int((input_ranges[i][1] - input_ranges[i][0]) / input_resolution[i])
                    + 1
                )

            # Categorical variable setup
            if input_types[i] == VarType.CATEGORICAL:
                if len(input_ranges[i]) != len(set(input_ranges[i])):
                    raise CategoricalException(
                        f"input_ranges[{i}] must have unique values for categorical variable {input_names[i]}"
                    )
                if len(input_ranges[i]) < 1:
                    raise RangeException(
                        f"input_ranges[{i}] must have length >=1 for categorical variable {input_names[i]}"
                    )
                self._categories[i] = np.array(input_ranges[i])
                input_resolution[i] = len(self._categories[i])
                input_ranges[i] = [0, input_resolution[i] - 1]
                self._has_categorical = True

        # Validate input resolution
        if len(input_resolution) != self.input_dim:
            raise MissmatchDimensionException(
                f"input_resolution must have length {self.input_dim} but has length {len(input_resolution)}"
            )
        self._input_resolution = np.array(input_resolution)
        self._resolution_grids = []
        for d in range(self.input_dim):
            if self._input_resolution[d] is not None:
                self._resolution_grids.append(
                    np.linspace(
                        input_ranges[d][0],
                        input_ranges[d][1],
                        self._input_resolution[d],
                    )
                )
            else:
                self._resolution_grids.append(None)

        self._input_names = np.array(input_names)
        self._input_ranges = np.array(input_ranges)
        self._output_names = np.array(output_names)

    @property
    def categorical_indices(self) -> List[int]:
        """
        Get indices of categorical variables.

        Returns:
            List[int]: Indices of categorical variables in the input.
        """
        return [i for i, c in enumerate(self._categories) if c is not None]

    @property
    def categories(self) -> List[Union[None, np.ndarray]]:
        """
        Get unique categories for each categorical variable.

        Returns:
            List[Union[None, np.ndarray]]: List of unique categories for each categorical variable.
        """
        return [c if c is None else c.copy() for c in self._categories]

    def get_categories_from_index(self, index: int) -> Union[None, np.ndarray]:
        """
        Get categories of a categorical variable by its index.

        Args:
            index (int): Index of the categorical variable.

        Returns:
            Union[None, np.ndarray]: Categories of the specified variable or None if not categorical.
        """
        if not (0 <= index < self.input_dim):
            raise CategoricalException(
                f"index must be in range [0, {self.input_dim - 1}]"
            )
        return (
            None if self._categories[index] is None else self._categories[index].copy()
        )

    def raw_data_to_categorical_if_needed(
        self, x: np.ndarray, copy: bool = True
    ) -> np.ndarray | List[List[Any]]:
        """
        Convert raw data to categorical format if necessary.

        Args:
            x (np.ndarray): Input data array.
            copy (bool, optional): Whether to return a copy of the array. Defaults to True.

        Returns:
            np.ndarray | List[List[Any]]: Data array with categorical variables converted to
            categorical indices if all variables are numerical, otherwise a list of lists
            with the target values.
        """
        if not isinstance(x, np.ndarray):
            x = np.array(x)
            copy = False  # Don't copy if not a numpy array to avoid unnecessary copies
        if x.ndim != 2 or x.shape[1] < self.input_dim:
            raise MissmatchDimensionException(
                f"x must have shape (n_samples, >={self.input_dim}) but has shape {x.shape}"
            )
        if self._has_categorical:
            x = x.copy() if copy else x
            for i in self.categorical_indices:
                xi = x[:, i]
                catsi = self.get_categories_from_index(i)
                # check if xi is numerical
                if np.issubdtype(xi.dtype, np.number):
                    if np.all(xi == xi.astype(int)):
                        if xi.min() >= 0 and xi.max() < len(catsi):
                            # already categorical indices
                            continue
                if not np.issubdtype(catsi.dtype, np.number):
                    xi = xi.astype(catsi.dtype)

                # Convert to categorical indices
                replaced = np.zeros_like(xi, dtype=bool)
                for u in range(len(catsi)):
                    # Replace category values with their indices
                    mask = np.equal(xi, catsi[u])
                    xi[mask] = u
                    replaced = replaced | mask
                # Raise exception if any values were not replaced
                if not np.all(replaced):
                    raise CategoricalException(
                        f"input value {xi[~replaced]} not in category {catsi}"
                    )
                x[:, i] = xi

            # Convert to float only if not already a float array
            if x.dtype != float:
                x = x.astype(float)
        return x

    def categorical_index_to_raw_if_needed(
        self, x: np.ndarray, copy: bool = True
    ) -> np.ndarray | List[np.ndarray]:
        """
        Convert categorical indices back to their original raw values if needed.

        Args:
            x (np.ndarray): Input data array with categorical indices.
            copy (bool, optional): Whether to return a copy of the array. Defaults to True.

        Returns:
            np.ndarray: Data array with categorical indices converted back to original values.
        """
        if not isinstance(x, np.ndarray):
            x = np.array(x)
            copy = False  # Don't copy if not a numpy array to avoid unnecessary copies
        if x.ndim != 2 or x.shape[1] < self.input_dim:
            raise MissmatchDimensionException(
                f"x must have shape (n_samples, >={self.input_dim})"
            )
        if self._has_categorical:
            x = x.copy() if copy else x
            _x = [x[:, i] for i in range(self.input_dim)]
            all_numeric = True
            for i in self.categorical_indices:
                xi = _x[i].round().astype(int)
                catsi = self.get_categories_from_index(i)
                xi = catsi[xi]
                _x[i] = xi
                if all_numeric and not np.issubdtype(xi.dtype, np.number):
                    all_numeric = False
            if all_numeric:
                for i in range(self.input_dim):
                    x[:, i] = _x[i]

            else:
                x = [
                    [_x[i][l] for i in range(self.input_dim)] for l in range(x.shape[0])
                ]

        return x

    @property
    def input_dim(self) -> int:
        """
        The dimensionality of the input space.

        Returns:
            int: The number of input variables.
        """
        return self._input_dim

    @property
    def output_dim(self) -> int:
        """
        The dimensionality of the output space.

        Returns:
            int: The number of output variables.
        """
        return self._output_dim

    @property
    def dim(self) -> int:
        """
        Total dimensionality of the problem (input + output).

        Returns:
            int: The sum of input and output dimensions.
        """
        return self.input_dim + self.output_dim

    @property
    def input_names(self) -> np.ndarray:
        """
        Names of the input variables.

        Returns:
            np.ndarray: An array containing the names of input variables.
        """
        return self._input_names.copy()

    @property
    def output_names(self) -> np.ndarray:
        """
        Names of the output variables.

        Returns:
            np.ndarray: An array containing the names of output variables.
        """
        return self._output_names.copy()

    @property
    def names(self) -> np.ndarray:
        """
        Combined names of both input and output variables.

        Returns:
            np.ndarray: An array containing names of both input and output variables.
        """
        return np.concatenate((self.input_names, self.output_names))

    @property
    def input_types(self) -> List[VarType]:
        """
        Types of the input variables.

        Returns:
            List[VarType]: A list of enumeration members representing the types of input variables.
        """
        return self._input_types.copy()

    @property
    def input_ranges(self) -> np.ndarray:
        """
        Ranges of the input variables.

        Returns:
            np.ndarray: An array of ranges for each input variable.
        """
        return self._input_ranges.copy()

    @property
    def input_resolution(self) -> np.ndarray:
        """
        Resolution for each input variable.

        Returns:
            np.ndarray: An array containing the resolution for each input variable.
        """
        return self._input_resolution.copy()


class RandomStateMixin:
    def __init__(self, *args, seed: int = None, **kwargs):
        """
        Initialize the RandomStateMixin object.

        Args:
            *args: Variable length argument list.
            seed (int, optional): The seed for the random number generator. If None, a random seed is chosen.
            **kwargs: Arbitrary keyword arguments.
        """
        # Set seed to a random integer if None, ensuring it's an integer
        self._seed = int(seed) if seed is not None else np.random.randint(1, 1e6)

        self.rand_reset()

        super().__init__(*args, **kwargs)

    def rand_reset(self):
        """
        Reset the random number generator with the current seed.
        """
        self.rnd_gen = np.random.RandomState(self._seed)

    @property
    def seed(self) -> int:
        """
        Get the seed value.

        Returns:
            int: The seed value.
        """
        return self._seed


class DuplicatePointHandler:
    """
    Abstract base class for handling duplicate points in optimization problems.
    """

    def handle_duplicate_points(
        self, optimizer, all_points: np.ndarray, duplicate_indices: List[int]
    ) -> None:
        """
        Abstract method to handle duplicate points. This method must be implemented in subclasses.

        Args:
            optimizer: The optimizer instance.
            all_points (np.ndarray): Array of all points.
            duplicate_indices (List[int]): Indices of duplicate points.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError(
            "handle_duplicate_point must be implemented in a DuplicatePointHandler subclass"
        )

    def __call__(
        self,
        optimizer: Optimizer,
        all_points: np.ndarray,
        duplicate_indices: Optional[List[int]] = None,
    ) -> Any:
        """
        Invoke the handler to process duplicate points.

        Args:
            optimizer: The optimizer instance.
            all_points (np.ndarray): Array of all points.
            duplicate_indices (List[int]): Indices of duplicate points.

        Returns:
            Any: Result from handling duplicate points.
        """
        if duplicate_indices is None:
            duplicate_indices = optimizer.get_duplicate_points_index(all_points)

        if len(duplicate_indices) == 0:
            return all_points
        return self.handle_duplicate_points(optimizer, all_points, duplicate_indices)


class DuplicatePointHandlerException(DuplicatePointHandler):
    """
    Handler that raises an exception when duplicate points are encountered.
    """

    def handle_duplicate_points(
        self, optimizer, all_points: np.ndarray, duplicate_indices: List[int]
    ) -> None:
        """
        Handles duplicate points by raising a ValueError.

        Args:
            optimizer: The optimizer instance.
            all_points (np.ndarray): Array of all points.
            duplicate_indices (List[int]): Indices of duplicate points.

        Raises:
            ValueError: If duplicate points are encountered.
        """

        raise ValueError(
            f"Points {all_points[duplicate_indices]} already exist in sampled data."
        )


class IgnoreDuplicatePointHandler(DuplicatePointHandler):
    """
    Handler that ignores duplicate points.
    """

    def handle_duplicate_points(
        self, optimizer, all_points: np.ndarray, duplicate_indices: List[int]
    ) -> None:
        """
        Handles duplicate points by ignoring them.

        Args:
            optimizer: The optimizer instance.
            all_points (np.ndarray): Array of all points.
            duplicate_indices (List[int]): Indices of duplicate points.
        """
        return all_points


class RandomPointDuplicatePointHandler(DuplicatePointHandler):
    """
    Handler that replaces duplicate points with random points within the optimizer's input ranges.
    """

    def handle_duplicate_points(
        self,
        optimizer: Optimizer,
        all_points: np.ndarray,
        duplicate_indices: List[int],
    ) -> np.ndarray:
        """
        Handles duplicate points by replacing them with random points.

        Args:
            optimizer: The optimizer instance.
            all_points (np.ndarray): Array of all points.
            duplicate_indices (List[int]): Indices of duplicate points.

        Returns:
            np.ndarray: Array of all points with duplicates replaced by random points.
        """

        n = len(duplicate_indices)
        if n == 0:
            return all_points
        sample_datapoints = np.zeros((n * 100, optimizer.input_dim))
        ub, lb = (
            optimizer.input_ranges[:, 0].astype(float),
            optimizer.input_ranges[:, 1].astype(float),
        )

        for i in range(optimizer.input_dim):
            sample_datapoints[:, i] = (
                optimizer.rnd_gen.rand(n * 100) * (ub[i] - lb[i]) + lb[i]
            )

        sample_datapoints = optimizer.map_points_to_resolution(
            sample_datapoints, unique=True
        )
        sample_datapoints = sample_datapoints[
            ~optimizer.get_duplicate_points_mask(sample_datapoints)
        ]
        sample_datapoints = sample_datapoints[:n]
        duplicate_indices = duplicate_indices[: len(sample_datapoints)]
        all_points[duplicate_indices] = sample_datapoints

        return all_points


DirectionType = Union[Literal["min", "max"], float]


# base class for optimizer
class Optimizer(RandomStateMixin, FixedVarBase):
    """
    Base class for optimizers with integrated random state management and fixed variable handling.
    """

    DEFAULT_DUPLICATE_POINT_HANDLER: (
        DuplicatePointHandler
    ) = RandomPointDuplicatePointHandler

    def __init__(
        self,
        *args,
        direction: DirectionType = "max",  # direction of optimization: "min", "max", or numeric target
        **kwargs,
    ) -> None:
        """
        Initialize the Optimizer.

        Args:
            *args: Variable length argument list.
            direction (str|float): Direction of optimization, either "min", "max", or a numeric target.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(
            *args,
            **kwargs,
        )

        self.duplicate_point_sampled = self.DEFAULT_DUPLICATE_POINT_HANDLER()

        # Internal method to reset the optimizer
        self.reset = self._create_reset_method()

        # Internal method to sample new points
        self.sample = self._create_sample_method()

        # reset the optimizer initially
        self.reset()

        # Validate direction parameter
        try:
            direction = float(direction)
        except ValueError:
            if direction not in ["min", "max"]:
                raise ValueError(
                    f"direction must be 'min', 'max', or a numeric target, but is '{direction}'"
                )
        self._direction = direction

    def _create_reset_method(self):
        """
        Create the reset method for the optimizer by overriding the original reset method.
        This is done to ensure reset()  also reset the the random state
        This method is called by the Optimizer constructor.


        Returns:
            Callable: The reset method.
        """

        original_reset = self.reset  # save original reset method

        def _reset():
            self.rand_reset()  # reset random state
            self._datapoints = np.zeros((0, self.input_dim + 1))  # reset datapoints
            original_reset()  # call original reset method

        return _reset

    def map_points_to_resolution(self, points: np.ndarray, unique=False) -> np.ndarray:
        for i in range(self.input_dim):
            if self._resolution_grids[i] is not None:
                pointsi = points[:, i]
                grid = self._resolution_grids[i]
                # Find the index in b for each element in a where the element in b is closest to the element in a
                closest_indices = np.searchsorted(grid, pointsi, side="left")
                # Handle edge cases: if the closest index is at the end of b, decrement it by 1
                closest_indices = np.clip(closest_indices, 0, len(grid) - 1)

                # Adjust indices where the lower neighbor in b is closer
                lower_neighbor_is_closer = (closest_indices > 0) & (
                    np.abs(pointsi - grid[closest_indices - 1])
                    < np.abs(pointsi - grid[closest_indices])
                )
                closest_indices[lower_neighbor_is_closer] -= 1

                # Replace values in a with the closest values from b
                points[:, i] = grid[closest_indices]

        # make points unique
        if unique:
            points = np.unique(points, axis=0)
        return points

    def get_duplicate_points_mask(self, points: np.ndarray, within=True):
        """Returns a mask for the given points where the values are True for
        the points that are already in the optimizer's datapoints"""
        in_dp = np.isin(
            points,
            self._datapoints[:, : self._input_dim],  # assume_unique=True
        ).all(1)

        if within:
            # check for repeated points within the points array
            # Get inverse mapping and counts of unique elements
            unique, inverse, counts = np.unique(
                points, return_inverse=True, return_counts=True, axis=0
            )
            # Create mask for duplicates
            is_not_unique = counts[inverse] > 1

            # set the first occurence of each duplicate to False
            _, first_indices = np.unique(inverse, return_index=True)
            is_not_unique[first_indices] = False

            in_dp = in_dp | is_not_unique

        return in_dp

    def get_duplicate_points_index(self, points: np.ndarray, within=True):
        mask = self.get_duplicate_points_mask(points, within=within)
        return np.where(mask)[0]

    def _create_sample_method(self):
        """
        Create the sample method for the optimizer by overriding the original sample method.
        This is done to ensure that duplicate points are handled.
        This method is called by the Optimizer constructor.

        Returns:
            Callable: The sample method.
        """
        original_sample_method = self.sample

        def sample_with_duplicate_check(*args, allow_duplicates=False, **kwargs):
            points: np.array = original_sample_method(
                *args, **kwargs
            )  # call original sample method

            # for each dimension check if a resolution is defined and if so map the points to the resolution
            points = self.map_points_to_resolution(points)

            # check if points are already in self._datapoints
            # get indices of duplicate points
            if not allow_duplicates:
                dulicate_indices = self.get_duplicate_points_index(points)
                if len(dulicate_indices) > 0:
                    points = self.duplicate_point_sampled(
                        self, points, dulicate_indices
                    )  # handle duplicate points

                points = points[~self.get_duplicate_points_mask(points)]

            return points  # return sampled points

        return sample_with_duplicate_check

    @property
    def direction(self) -> DirectionType:
        """Return the optimization direction."""
        return self._direction

    def reset(self) -> None:
        """Reset the optimizer to an unfitted state. This method should be implemented by subclasses."""
        raise NotImplementedError()

    def fit(self, data: np.ndarray, append: bool = True) -> None:
        """
        Fit the optimizer with data.

        Args:
            data (np.ndarray): Data array containing single points in parameter space including outcomes. The shape of the array must be (n_samples, input_dim + output_dim).
            append (bool): Whether to append the new data to existing data or replace it.
        """

        if not isinstance(data, np.ndarray):
            data = np.array(data)
        # check if data has correct shape
        if data.ndim != 2 or data.shape[1] != self.dim:
            raise MissmatchDimensionException(
                f"data must have shape (n_samples, {self.dim}({self.input_dim}+{self.output_dim}))"
            )

        # reset the optimizer if append is False
        if not append:
            self.reset()

        # add data to datapoints
        self._datapoints = np.concatenate((self._datapoints, data), axis=0)
        if self.__class__.fit == Optimizer.fit:
            raise NotImplementedError()

    @property
    def datapoints(self) -> np.ndarray:
        """Return a copy of the datapoints."""
        return self._datapoints.copy()

    @property
    def intrinsic_datapoints(self) -> np.ndarray:
        """Return intrinsic datapoints, converting raw data to categorical format if needed."""
        return self.raw_data_to_categorical_if_needed(self.datapoints, copy=False)

    def sample(self, n: int):
        """
        Sample new points.

        Args:
            n (int): Number of new points to sample.

        Returns:
            np.ndarray: Sampled points.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError()


class Model(FixedVarBase):
    """
    Base class for models, can also be used for optimizers if they are model based.
    Provides functionality to generate grids of points and evaluate models.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Model instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def _generate_resolution(self, resolution) -> np.ndarray[[-1], int]:
        # Set default resolution for each dimension if not provided
        if resolution is None:
            resolution = self.input_resolution

        if isinstance(resolution, np.ndarray):
            # Convert 0-dimensional numpy array to integer
            if resolution.ndim == 0:
                resolution = int(resolution)

        if isinstance(resolution, float):
            # Convert float resolution to integer
            resolution = int(resolution)

        if isinstance(resolution, (int, np.int32, np.int64)):
            # Use the provided integer resolution for each dimension
            resolution = [resolution] * self.input_dim

        # Ensure resolution array is not shorter than the number of input dimensions
        if len(resolution) < self.input_dim:
            raise MissmatchDimensionException(
                f"resolution must have length >= {self.input_dim} but has length {len(resolution)}"
            )
        resolution = resolution[: self.input_dim]

        # Fill in None values in resolution with model's default resolutions
        _resolution = self.input_resolution

        for i in range(self.input_dim):
            if resolution[i] is None:
                resolution[i] = _resolution[i]

        # Ensure resolution for categorical variables matches the number of categories
        for ci in self.categorical_indices:
            resolution[ci] = self.input_resolution[ci]

        # Set default resolution for any remaining None values
        for i in range(self.input_dim):
            if resolution[i] is None:
                resolution[i] = DEFAULT_RESOLUTION

        resolution = np.array(resolution)
        if np.any(resolution <= 0):
            raise ResolutionException(
                f"resolution must consist of positive integers but is {resolution}"
            )
        return resolution

    def get_grid(
        self, resolution=None, evaluated=True, input_ranges=None
    ) -> np.ndarray:
        """
        Get a grid of points for the problem.

        Args:
            resolution (Optional[Union[int, List[int], np.ndarray]]): The number of points in each dimension.
            evaluated (bool): Whether to evaluate the function at the grid points.
            input_ranges (Optional[np.ndarray]): Specific input ranges to use. If None, uses the model's input ranges.

        Returns:
            np.ndarray: A numpy array of the grid points.

        Raises:
            AssertionError: If the input_ranges are not properly formatted.

        Returns:
            np.ndarray: A numpy array of the grid points with shape (*[resolution[i] for i in range(self.input_dim)],len(self.input_dim))
            or (*[resolution[i] for i in range(self.input_dim)],self.output_dim,len(self.input_dim)+len(self.output_dim)) if evaluated is True.
        """

        # Use model's input ranges if none are provided
        if input_ranges is None:
            input_ranges = self._input_ranges

        if not isinstance(input_ranges, np.ndarray):
            input_ranges = np.array(input_ranges)

        if input_ranges.ndim != 2:
            raise MissmatchDimensionException(
                f"input_ranges must have shape ({self._input_dim},2) but has shape {input_ranges.shape}"
            )

        if input_ranges.shape[1] != 2:
            raise RangeException(
                f"input_ranges must have shape ({self._input_dim},2) but has shape {input_ranges.shape}"
            )

        if len(input_ranges) < self.input_dim:
            input_ranges = np.concatenate(
                (input_ranges, self._input_ranges[len(input_ranges) :]), axis=0
            )

        # Override input ranges for categorical variables with model's own ranges
        if self._has_categorical:
            for i in self.categorical_indices:
                input_ranges[i] = self._input_ranges[i]

        # Ensure input_ranges is a 2D array with shape (input_dim, 2)

        if input_ranges.shape[0] != self._input_dim:
            raise RangeException(
                f"input_ranges must have shape ({self._input_dim},2) but has shape {input_ranges.shape}"
            )

        resolution = self._generate_resolution(resolution)
        # If evaluated is True, use get_grid_points to generate and evaluate the grid
        if evaluated:
            gp = self.get_grid_points(
                resolution=resolution,
                evaluated=evaluated,
                input_ranges=input_ranges,
                grid_shape=True,
            )

            return gp

        # Generate grid points using numpy's linspace and meshgrid functions
        x = [
            np.linspace(input_ranges[d, 0], input_ranges[d, 1], resolution[d])
            for d in range(self.input_dim)
        ]

        return np.stack(np.meshgrid(*x, indexing="ij"), axis=-1)

    def get_grid_points(
        self,
        resolution=None,
        evaluated=True,
        grid_shape=True,
        input_ranges=None,
        replace_categorical_indices=False,
    ) -> np.ndarray:
        """
        Get a grid of points for the problem, optionally evaluating them.

        Args:
            resolution (Optional[Union[int, List[int], np.ndarray]]): The number of points in each dimension.
            evaluated (bool): Whether to evaluate the function at the grid points.
            grid_shape (bool): Whether to return the grid in its original shape.
            input_ranges (Optional[np.ndarray]): Specific input ranges to use.

        Returns:
            np.ndarray: A numpy array of the grid points, optionally evaluated.
        """

        # gets the simple coordinate grid without evaluation
        g = self.get_grid(
            resolution=resolution, evaluated=False, input_ranges=input_ranges
        )

        oshape = g.shape[:-1]  # store the grids shape

        # reshape to list of points [[x1,y1,z1,...],[x2,y2,z2,...],...]

        # g has shape (*resolution,input_dim) and should be reshaped to (*resolution,input_dim)
        g = g.reshape(-1, self.input_dim)

        # tarnsfer categorical variables to original values
        if replace_categorical_indices:
            g = self.categorical_index_to_raw_if_needed(g, copy=False)

        if evaluated:
            # evaluate the function at the grid points
            _y = self(g)
            g = np.concatenate((g, _y), axis=-1)  # add results to points

        # reshape to grid if needed

        if grid_shape:
            g = g.reshape(*oshape, self.input_dim + self.output_dim)

        return g

    def evaluate(self, x) -> np.ndarray:
        """
        Evaluate the model for given input points.

        Args:
            x (np.ndarray): Input points for evaluation, with shape (n_samples, input_dim)

        Returns:
            np.ndarray: Evaluated results.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("evaluate not implemented")

    def __call__(self, x, **kwargs) -> np.ndarray:
        """
        Make the model callable, allowing direct evaluation with input points.

        Args:
            x (np.ndarray): Input points for evaluation.
            **kwargs: Additional keyword arguments.

        Returns:
            np.ndarray: Evaluated results.
        """
        x, revai = self._auto_input_dim(x)
        y = self.evaluate(x, **kwargs)
        res = None
        if isinstance(y, (tuple)):
            fy = y
            y = fy[0]
            res = fy[1:]
            if len(res) == 1:
                res = res[0]
        y = self._auto_output_dim(y, revai)

        if res is not None:
            return y, res
        return y

    def _auto_output_dim(self, y, revai):
        """
        Ensure that the output has the correct shape.

        Args:
            y (np.ndarray): The output data.
            revai (List[Callable]): List of functions to reverse operations on the output.

        Returns:
            np.ndarray: Output data with the correct shape.
        """
        y = np.array(y)
        if y.ndim == 0:
            y = y[None, None]
        if y.ndim == 1:
            y = y[:, None]

        for f in reversed(revai):
            y = f(y)
        return y

    def _auto_input_dim(self, x):
        """
        Ensure that the input has the correct shape and convert categorical data if necessary.

        Args:
            x (np.ndarray): The input data.

        Returns:
            Tuple[np.ndarray, List[Callable]]: Processed input data and a list of functions to reverse
            operations on the output.
        """
        reverse_op = []
        x = np.array(x)
        if x.ndim == 0:
            x = x[None]
        if x.ndim == 1:
            x = x.reshape(-1, self.input_dim)
        if x.ndim > 2:
            if x.ndim != self.input_dim + 1:
                raise MissmatchDimensionException(
                    f"input dimension {x.ndim} does not match model input dimension for a grid {self.input_dim+1}"
                )

            if x.shape[-1] != self.input_dim:
                raise MissmatchDimensionException(
                    f"input dimension {x.shape[-1]} does not match model input dimension {self.input_dim},"
                    + "when using a grid the last dimension must be the input dimension"
                )

            exp_shape = x.shape[:-1] + (self.output_dim,)
            reverse_op.append(lambda y: y.reshape(exp_shape))
            x = x.reshape(-1, self.input_dim)

        if x.shape[1] != self.input_dim:
            raise MissmatchDimensionException(
                f"input dimension {x.shape[1]} does not match model input dimension {self.input_dim}"
            )
        x = self.raw_data_to_categorical_if_needed(x, copy=False)
        return x, reverse_op
