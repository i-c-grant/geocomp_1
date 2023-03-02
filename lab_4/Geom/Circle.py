from .Geom import Geom
from .Shape import Shape
from .Point import Point

import math as mth


class Circle(Shape):
    def __init__(self, blueprint: list):
        self.geomType = "Circle"
        # Shape __init__() invokes the construct method to obtain the description
        super().__init__(blueprint)

    def constructPoints(self, blueprint: list):
        """Takes a list [Point, int or float], where Point is the center and float is
        the radius."""

        # Ensure that blueprint is of the correct format; radius must be > 0
        isList = type(blueprint) == list
        isPoint = type(blueprint[0]) == Point
        isRad = type(blueprint[1]) == int or type(blueprint[1]) == float

        if not (isList and isPoint and isRad):
            raise TypeError

        if len(blueprint) != 2 or blueprint[1] <= 0:
            raise ValueError

        # Return points list containing only the circle's center
        points = [blueprint[0]]
        return points

    def constructProperties(self, blueprint: list, points: list):
        """"""
        props : dict = {}
        props["center"] = blueprint[0]
        props["radius"] = blueprint[1]

        # Cannot call props.area() to set props["area"] because
        # self.properties["area"] is not yet set.
        props["area"] = mth.pi * props["radius"] ** 2 
        
        return props
    
    # Can be used to recalculate area if radius changes
    def area(self): 
        return mth.pi ** self.properties["radius"] ** 2
