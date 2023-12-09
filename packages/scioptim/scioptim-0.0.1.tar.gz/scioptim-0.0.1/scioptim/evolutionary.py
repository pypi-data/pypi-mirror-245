from scioptim.base import (
    Optimizer,
    Model,
    DuplicatePointHandler,
    DuplicatePointHandlerException,
    RandomPointDuplicatePointHandler,
)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import multivariate_normal

from scipy.optimize import (
    differential_evolution,
)  # see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html
from scipy.optimize import rosen
from scipy.stats.qmc import LatinHypercube
from scipy.stats.qmc import scale
from scioptim.test_objectives.pybenchfunction.function import Rosenbrock


class DifferentialEvolution(Optimizer):
    def __init__(self, input_samples, input_iterations, *args, **kwargs):
        # self._input_ranges = input_ranges
        self.input_samples = input_samples
        self.pop = []
        self.scores = []
        self.input_iterations = input_iterations

        super().__init__(*args, **kwargs)
        self.updated_seed = self.seed

    def reset(self):
        pass

    # updates the seed for multiple calls of the function "Optimization" (below)
    def set_seed(self):
        self.updated_seed += self.updated_seed

    # get the populations
    def get_pop(self):
        return self.pop

    # get the scores corresponding to the populations
    def get_scores(self):
        return self.scores

    # n = number of wanted output values
    def sample(self):
        sampler = LatinHypercube(d=self.input_dim, seed=self.seed)
        sample = sampler.random(n=self.input_samples)
        sample = scale(sample, self.input_ranges[:, 0], self.input_ranges[:, 1])
        return sample

    # define a customized Rosenbruck function that saves the populations and scores of each iteration
    def rosen_(self, x):
        self.pop.append(x)
        sol = rosen(x)
        self.scores.append(sol)
        return sol

    # The normal function that does not need to be called multiple times because of waiting time of measurements
    def normalOptimization(self, func):
        solution = differential_evolution(
            func,
            bounds=self.input_ranges,
            maxiter=self.input_iterations,
            init=self.sample(),
            seed=self.seed,
            polish=False,
        )
        return solution

    # The modified function that can be called multiple times due to waiting times for measurements
    # (updated seed will be updated automatically with set_seed())
    def Optimization(self, func):
        solution = differential_evolution(
            func,
            bounds=self.input_ranges,
            maxiter=1,
            init=self.sample(),
            seed=self.updated_seed,
            polish=False,
        )
        self.set_seed()
        return solution

    def Optimization2(self, func, ini):
        solution = differential_evolution(
            func,
            bounds=self.input_ranges,
            maxiter=1,
            init=ini,
            seed=self.updated_seed,
            polish=False,
        )
        self.set_seed()
        return solution

    def makeFigure(self):
        X, Y = np.linspace(-10, 10, 1000), np.linspace(-10, 10, 1000)
        X, Y = np.meshgrid(X, Y)
        XY = np.array([X, Y])
        Z = np.apply_along_axis(rosen, 0, XY)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # add contours and contours lines
        # ax.contour(X, Y, Z, levels=30, linewidths=0.5, colors='#999')
        cmap = [(0, "#2f9599"), (0.45, "#eeeeee"), (1, "#8800ff")]
        cmap = cm.colors.LinearSegmentedColormap.from_list("Custom", cmap, N=256)
        ax.contourf(X, Y, Z, levels=30, cmap=cmap, alpha=0.7)
        ax.scatter(sample[:, 0], sample[:, 1], c="red")
        ax.scatter(opt2.x[0], opt2.x[1])
        ax.scatter(1, 1, c="green")

        # add labels and set equal aspect ratio
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_aspect(aspect="equal")
        plt.show()
