import deepxde as dde
import abc
from functools import wraps


def run_if_all_none(*attr):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            x = [getattr(self, a) for a in attr]
            if all(i is None for i in x):
                return func(self, *args, **kwargs)
            return x if len(x) > 1 else x[0]

        return wrapper

    return decorator


class Data(abc.ABC):
    """Data base class."""

    def losses(self, targets, outputs, loss_fn, inputs, model, aux=None):
        """Return a list of losses, i.e., constraints."""
        raise NotImplementedError("Data.losses is not implemented.")

    def losses_train(self, targets, outputs, loss_fn, inputs, model, aux=None):
        """Return a list of losses for training dataset, i.e., constraints."""
        return self.losses(targets, outputs, loss_fn, inputs, model, aux=aux)

    def losses_test(self, targets, outputs, loss_fn, inputs, model, aux=None):
        """Return a list of losses for test dataset, i.e., constraints."""
        return self.losses(targets, outputs, loss_fn, inputs, model, aux=aux)

    # @abc.abstractmethod
    def train_next_batch(self, batch_size=None):
        """Return a training dataset of the size `batch_size`."""

    # @abc.abstractmethod
    def test(self):
        """Return a test dataset."""


class Tuple(Data):
    """Dataset with each data point as a tuple.

    Each data tuple is split into two parts: input tuple (x) and output tuple (y).
    """

    def __init__(self, train_x, train_y, test_x, test_y):
        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y

    def losses(self, targets, outputs, loss_fn, inputs, model, aux=None):
        return loss_fn(targets, outputs)

    def train_next_batch(self, batch_size=None):
        return self.train_x, self.train_y

    def test(self):
        return self.test_x, self.test_y


class Settings(Data):
    
    def __init__(self, geom, pde, boundary_condition, num_domain=3000, num_boundary=500, num_test=1000, train_distribution='LHS'):
        self.geom = geom
        self.pde = pde
        self.boundary_condition = boundary_condition
        self.num_domain = num_domain
        self.num_boundary = num_boundary
        self.num_test = num_test
        self.train_distribution = train_distribution
    
    def data(self):
        return dde.data.PDE(self.geom, self.pde, self.boundary_condition, num_domain=self.num_domain, num_boundary=self.num_boundary, num_test=self.num_test, train_distribution=self.train_distribution)
    
    
        
