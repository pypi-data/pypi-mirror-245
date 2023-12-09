import numpy as np
from scipy.stats import gaussian_kde
from scioptim import Optimizer
from scioptim.utils import normalize


###
def all_combinations(x1, x2):
    assert len(x1) == len(x2), "x1 and x2 must have the same length"
    n_dim = len(x1)
    target = np.zeros((2**n_dim, n_dim))
    for i in range(n_dim):
        target[:, i] = np.tile(np.repeat([x1[i], x2[i]], 2 ** (n_dim - 1 - i)), 2**i)

    return target


#######################################
###                                 ###
###            Algorithms           ###
###                                 ###
#######################################


#######################################
###
###   1. Random Search Optimizer Class
###
#######################################
class RandomSearch(Optimizer):
    def reset(self):
        # TODO: kann raus?
        self._sample_bounds_lower, self._sample_bounds_upper = (
            self.input_ranges[:, 0].astype(float),
            self.input_ranges[:, 1].astype(float),
        )

    # n = number of wanted output values
    def sample(self, n: int):
        sample_datapoints = np.zeros((n, self.input_dim))
        ub, lb = (
            self.input_ranges[:, 0].astype(float),
            self.input_ranges[:, 1].astype(float),
        )
        for i in range(self.input_dim):
            sample_datapoints[:, i] = self.rnd_gen.rand(n) * (ub[i] - lb[i]) + lb[i]

        return sample_datapoints

    # not nescessary for fully random search
    def fit(self, data, append=True):
        super().fit(data, append=append)


#######################################
###
###   2. Latin-Hypercube Sampler Class
###
#######################################
# currentlx not working properly due to the fact that the latin hypercube sampling is not usable fpr single point sampling
# from scipy.stats.qmc import LatinHypercube
# from scipy.stats.qmc import scale


# class LatinHypercubeSearch(Optimizer):
#    def reset(self):
#        self._sampler = LatinHypercube(d=self.input_dim)

# n = number of wanted output values
#   def sample(self, n: int):
#       sample = self._sampler.random(n=n)
#       sample = scale(sample, self.input_ranges[:, 0], self.input_ranges[:, 1])
#       return sample


#######################################
###
###   3. Greedy Zoom Optimizer Class
###
#######################################
class GreedyRandomZoom(Optimizer):
    def reset_bounds(self):
        self._sample_bounds_lower, self._sample_bounds_upper = (
            self.input_ranges[:, 0].astype(float),
            self.input_ranges[:, 1].astype(float),
        )

    def reset(self):
        self.reset_bounds()
        bp = all_combinations(self._sample_bounds_lower, self._sample_bounds_upper)
        self._bp = np.concatenate([bp.T, [[-np.inf] * bp.shape[0]]], axis=0).T

    @property
    def sample_bounds(self):
        return self._sample_bounds_lower.copy(), self._sample_bounds_upper.copy()

    def sample(self, n: int):
        sample_datapoints = np.zeros((n, self.input_dim))
        ub, lb = self.sample_bounds
        if np.allclose(ub, lb):
            if np.allclose(
                normalize(ub, self.input_ranges),
                normalize(lb, self.input_ranges),
                rtol=1e-10,
            ):
                self.reset_bounds()
                ub, lb = self.sample_bounds
        for i in range(self.input_dim):
            sample_datapoints[:, i] = self.rnd_gen.rand(n) * (ub[i] - lb[i]) + lb[i]

        return sample_datapoints

    def fit(self, data, append=True):
        super().fit(data, append=append)

        if len(data) == 0:
            return
        self._bp = np.concatenate([data, self._bp], axis=0)

        if self.direction == "max":
            self._bp = self._bp[np.argsort(self._bp[..., -1])[::-1]]
        elif self.direction == "min":
            self._bp = self._bp[np.argsort(self._bp[..., -1])]
        else:
            # towards point
            self._bp = self._bp[np.argsort(np.abs(self._bp[..., -1] - self.direction))]

        best_point = self._bp[0]

        new_lb, new_ub = self.sample_bounds
        for i in range(self.input_dim):
            smaller_p = self._bp[:, i]

            smaller_p = smaller_p[smaller_p < best_point[i]]

            if len(smaller_p) > 0:
                new_lb[i] = smaller_p.max()
            else:
                new_lb[i] = best_point[i]
            larger_p = self._bp[:, i][self._bp[:, i] > best_point[i]]

            if len(larger_p) > 0:
                new_ub[i] = larger_p.min()
            else:
                new_ub[i] = best_point[i]

        self._sample_bounds_lower, self._sample_bounds_upper = new_lb, new_ub
