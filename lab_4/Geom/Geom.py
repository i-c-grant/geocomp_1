import random


class Geom:
    geomType = "Generic Geometry Type"

    # Constructor of the class: used to initialize an object
    def __init__(self):
        # Check out the names and the faker packages for random names
        self.name = random.choice(
            ["Bill", "Sally", "Tamica", "Josh", "Lammar", "Hussain"]
        )
        self.color = random.choice(["BLUE", "RED", "PURPLE"])

    # This is a method that all children will inherit.
    # In other words, all children will have this method without explicitly defining it.
    def print_name(self):
        print(self.makeString())

    # Another method: why we can call self.area without defining it here?
    def makeString(self):
        return f"I am a {self.geomType} named {self.name}. My color is {self.color}."
