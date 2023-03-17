from .Geom import Geom
from .Vector import Vector
from .Point import Point
import numpy as np

class Shape(Geom):
    """"""

    # List containing the information from which the Shape is constructed
    blueprint: list = []
    # List containing all the Points of the Shape
    points: list = []
    # Dict containing all the properties of the Shape (e.g. radius, side length)
    # Keys vary depending on subclass of Shape
    properties: dict = {}

    def __init__(self, blueprint: list):
        """"""
        # Set the "blueprint" attribute to preserve a record of the
        # information used to construct the shape
        self.blueprint = blueprint
        # Set the points list using subclass method
        self.points = self.constructPoints(blueprint)
        # Set the properties dict using subclass method;
        self.properties = self.constructProperties(blueprint, self.points)
        # self.desc = self.construct(blueprint)
        super().__init__()

    def coordsList(self):
        return [corner.coords for corner in self.points]

    def translate(self, vector: Vector):
        """Translates the shape according to vector."""

        for i in range(len(self.points)):
            oldx = self.points[i].x
            oldy = self.points[i].y
            
            magnitude = vector.magnitude
            direction = vector.direction

            # Approximate trig functions because to avoid getting very
            # small values instead of 0 (e.g. for sin(180))
            approx_cos = np.around(np.cos(np.radians(direction)), decimals=5)
            approx_sin = np.around(np.sin(np.radians(direction)), decimals=5)

            newx = oldx + vector.magnitude * approx_cos
            newy = oldy + vector.magnitude * approx_sin

            self.points[i] = Point([newx, newy])

    def constructPoints(self, blueprint):
        """"""
        raise BaseException

    def constructProperties(self, blueprint):
        """"""
        raise BaseException








        
        
        
