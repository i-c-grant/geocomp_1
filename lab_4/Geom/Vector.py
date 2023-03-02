from .Geom import Geom

class Vector(Geom):

    def __init__(self, description: list):
        """"""
        if type(description) != list:
            raise TypeError
        
        magnitude: float = float(description[0])
        direction: float = float(description[1])
        
        self.geomType = "Vector"
        self.magnitude = magnitude
        self.direction = direction
        super().__init__()
