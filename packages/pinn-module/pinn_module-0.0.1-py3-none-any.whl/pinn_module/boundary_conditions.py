import deepxde as dde
import numpy as np
import torch
from functools import wraps
from abc import ABC, abstractmethod


class BC(ABC):
    """Boundary condition base class.

    Args:
        geom: A ``deepxde.geometry.Geometry`` instance.
        on_boundary: A function: (x, Geometry.on_boundary(x)) -> True/False.
        component: The output component satisfying this BC.
    """

    def __init__(self, geom, on_boundary, component):
        self.geom = geom
        self.on_boundary = lambda x, on: np.array([on_boundary(x[i], on[i]) for i in range(len(x))])
        self.component = component

    def filter(self, X):
        return X[self.on_boundary(X, self.geom.on_boundary(X))]

    def collocation_points(self, X):
        return self.filter(X)

    @abstractmethod
    def error(self, X, inputs, outputs, beg, end, aux_var=None):
        """Returns the loss."""
        # aux_var is used in PI-DeepONet, where aux_var is the input function evaluated
        # at x.


def return_tensor(func):
    """Convert the output to a Tensor."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return torch.as_tensor(func(*args, **kwargs))

    return wrapper


def npfunc_range_autocache(func):
    """Call a NumPy function on a range of the input ndarray.

    If the backend is pytorch, the results are cached based on the id of X.
    """

    cache = {}

    @wraps(func)
    def wrapper_nocache(X, beg, end, variable, _):
        return func(X[beg:end], variable)

    @wraps(func)
    def wrapper_nocache_auxiliary(X, beg, end, variable, aux_var):
        return func(X[beg:end], variable, aux_var[beg:end])

    @wraps(func)
    def wrapper_cache(X, beg, end):
        key = (id(X), beg, end)
        if key not in cache:
            cache[key] = func(X[beg:end])
        return cache[key]

    @wraps(func)
    def wrapper_cache_auxiliary(X, beg, end, aux_var):
        # Even if X is the same one, aux_var could be different
        key = (id(X), beg, end)
        if key not in cache:
            cache[key] = func(X[beg:end], aux_var[beg:end])
        return cache[key]

    # if utils.get_num_args(func) == 1:
    # return wrapper_nocache
    # if utils.get_num_args(func) == 2:
    return wrapper_cache


class DirichletBC(BC):
    """Dirichlet boundary conditions: y(x) = func(x)."""

    def __init__(self, geom, func, on_boundary, component=0):
        super().__init__(geom, on_boundary, component)
        self.func = npfunc_range_autocache(return_tensor(func))
        
    def error(self, X, inputs, outputs, beg, end, aux_var=None):
        values = self.func(X, beg, end)
        
        return outputs[beg:end, self.component : self.component + 1] - values


class NeumannBC(BC):
    """Neumann boundary conditions: dy/dn(x) = func(x)."""

    def __init__(self, geom, func, on_boundary, component=0):
        super().__init__(geom, on_boundary, component)
        self.func = npfunc_range_autocache(return_tensor(func))

    def error(self, X, inputs, outputs, beg, end, aux_var=None):
        values = self.func(X, beg, end, aux_var)
        return self.normal_derivative(X, inputs, outputs, beg, end) - values


class RobinBC(BC):
    """Robin boundary conditions: dy/dn(x) = func(x, y)."""

    def __init__(self, geom, func, on_boundary,component=0):
        super().__init__(geom, on_boundary, component)
        self.func = func

    def error(self, X, inputs, outputs, beg, end, aux_var=None):
        return self.normal_derivative(X, inputs, outputs, beg, end) - self.func(
            X[beg:end], outputs[beg:end]
        )


def boundary_counditions(bc_type, geom, func, on_boundary, component=0):
    if bc_type == "dirichlet":
        return DirichletBC(geom, func, on_boundary,  component)
    elif bc_type == "neumann":
        return NeumannBC(geom, func, on_boundary, component)
    elif bc_type == "robin":
        return RobinBC(geom, func, on_boundary, component)
    else:
        raise NotImplementedError(f"{bc_type} is not implemented yet")


# def boundary_wall(X, on_boundary, D):
#     on_wall = np.logical_and(
#         np.logical_or(np.isclose(X[1], -D / 2), np.isclose(X[1], D / 2)), on_boundary
#     )  # +- D/2
#     return on_wall


# def boundary_inlet(X, on_boundary, L):
#     return on_boundary and np.isclose(X[0], -L / 2)  # -L/2


# def boundary_outlet(X, on_boundary, L):
#     return on_boundary and np.isclose(X[0], L / 2)  # L/2


def geometry(kwargs, type="rectangle"):
    if type == "rectangle":
        return dde.geometry.Rectangle(**kwargs)
    elif type == "star":
        return dde.geometry.StarShaped(**kwargs)
    elif type == "triangle":
        return dde.geometry.Triangle(**kwargs)
