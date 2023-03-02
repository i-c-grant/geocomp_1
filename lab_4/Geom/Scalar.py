from .Geom import Geom

class Scalar(Geom):
    """Geometric scalar."""
    def __init__(self, magnitude):
        self.magnitude = magnitude
        super().__init__()

    def val(self):
        return self.magnitude

    def printval(self):
        print(self.magnitude)

