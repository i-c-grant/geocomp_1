from .Geom import Geom
from .Shape import Shape
from .Point import Point

class Triangle(Shape):
    """"""

    def __init__(self, blueprint: list):
        self.geomType = "Triangle"

        # Shape __init__() invokes the construct method to obtain the description
        super().__init__(blueprint)

    def constructPoints(self, blueprint: list):
        """"""
        "Takes a list of three non-equivalent points."
        # Check that blueprint is a list of three points
        if type(blueprint) != list:
            raise TypeError

        for obj in blueprint:
            if type(obj) != Point:
                raise TypeError

        if len(blueprint) != 3:
            raise ValueError

        # Check that no two points in blueprint are equivalent
        for i in range(3):
            for c in range(3):
                if i == c:
                    break  # Don't check if a point is equivalent to itself
                else:
                    if blueprint[i].isEquivalent(blueprint[c]):
                        raise ValueError

        points = blueprint

        return points

    def constructProperties(self, blueprint, points: list):

        props : dict = {}
        
        x1 = points[0].x
        y1 = points[0].y

        x2 = points[1].x
        y2 = points[1].y

        x3 = points[2].x
        y3 = points[2].y

        props["side1"] = points[0].distance(points[1])
        props["side2"] = points[0].distance(points[2])
        props["side3"] = points[1].distance(points[2])
        props["area"] = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)

        return props
