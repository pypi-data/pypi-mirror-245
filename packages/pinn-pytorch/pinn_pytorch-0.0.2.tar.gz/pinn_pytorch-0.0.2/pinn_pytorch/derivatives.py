import torch 


class Jacobian:
    def __init__(self, ys, xs):
        self.ys = ys
        self.xs = xs

        self.dim_y = ys.shape[1]
        self.dim_x = xs.shape[1]

        self.J = {}

    def __call__(self, i=0, j=None):
        if not 0 <= i < self.dim_y:
            raise ValueError(f"i={i} is not valid.")
        if j is not None and not 0 <= j < self.dim_x:
            raise ValueError(f"j={j} is not valid.")

        if i not in self.J:
            y = self.ys[:, i:i + 1] if self.dim_y > 1 else self.ys
            self.J[i] = torch.autograd.grad(
                y,
                self.xs,
                grad_outputs=torch.ones_like(y),
                create_graph=True,
                allow_unused=True,
            )[0]
        return self.J[i] if j is None or self.dim_x == 1 else self.J[i][:, j:j + 1]


class Jacobians:
    def __init__(self):
        self.Js = {}
    def __call__(self, ys, xs, i=0, j=None):
        key = (ys, xs)

        if key not in self.Js:
            self.Js[key] = Jacobian(ys, xs)
        return self.Js[key](i, j)
    def clear(self):
        """Clear cached Jacobians."""
        self.Js = {}


class Hessian:
    def __init__(self, y, xs, component=None, grad_y=None):
        dim_y = y.shape[1]

        if dim_y > 1:
            if component is None:
                raise ValueError("The component of y is missing.")
            if component >= dim_y:
                raise ValueError(
                    f"The component of y={component} cannot be larger than the dimension={dim_y}."
                )
        else:
            if component is not None:
                raise ValueError("Do not use component for 1D y.")
            component = 0
        if grad_y is None:
            grad_y = Jacobians()(y, xs, i=component, j=None)
        self.H = Jacobian(grad_y, xs)

    def __call__(self, i=0, j=0):
        return self.H(i, j)


class Hessians:
    def __init__(self):
        self.Hs = {}
    def __call__(self, y, xs, component=None, i=0, j=0, grad_y=None):
        key = (y, xs, component)
        if key not in self.Hs:
            self.Hs[key] = Hessian(y, xs, component=component, grad_y=grad_y)
        return self.Hs[key](i, j)
    def clear(self):
        """Clear cached Hessians."""
        self.Hs = {}


def jacobian(y, x, i=0, j=None):
    return Jacobians()(y, x, i=i, j=j)


def hessian(y, xs, component=None, i=0, j=0, grad_y=None):
    return Hessians()(y, xs, component=component, i=i, j=j, grad_y=grad_y)
