import random

# define some vertex restriction methods for the Chaos Game

def noRestriction(point, points):
    return random.choice(points)

def avoidCurrent(point, points):
    oldPoint = point

    while (point := random.choice(points)) == oldPoint:
        pass

    return point

