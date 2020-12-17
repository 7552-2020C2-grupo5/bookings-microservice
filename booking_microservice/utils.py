"""Helper functions for the project."""


class FilterParam:
    """Filter a query based on an op and param"""

    def __init__(
        self, name, op, _in="query", schema="int", transform=None, format_=None
    ):
        self.name = name
        self.op = op
        self.val = None
        self.__schema__ = {"name": name, "in": _in, "type": schema, "format": format_}
        self.transform = transform

    def identity(self, x):
        return x

    def __call__(self, val):
        self.val = (self.transform or self.identity)(val)
        return self

    def apply(self, query, model):
        return query.filter(self.op(getattr(model, self.name), self.val))

    def __repr__(self):
        return f"filter {self.name} by {self.op}"

    def __str__(self):
        return self.__repr__()
