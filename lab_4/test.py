from Geom import Square, Circle, Point, Vector, Triangle

point1 = Point([0, 0])
point2 = Point([5, 5])
point3 = Point([6, 7])

# mySquare = Square([10])
# print(mySquare.area())
# print(mySquare.makeString())

myPoint = Point([2, 4])
print(myPoint.makeString())
print(myPoint.x, myPoint.y)

# myCircle = Circle([myPoint, 11])
# print(myCircle.area())
# print(myCircle.makeString())
# # myCircle.print_name()

myVector = Vector([5, 45])
print(myVector.makeString())
print(myVector.magnitude)
print(myVector.direction)

mySquare = Square([point1, point2])
myCircle = Circle([point1, 10])

print(myCircle.coordsList())
print(myCircle.properties["area"])
print(myCircle.properties["radius"])

myCircle.translate(myVector)

print(myCircle.coordsList())

print(mySquare.coordsList())

mySquare.translate(myVector)
print(mySquare.coordsList())



