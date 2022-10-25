from collections import namedtuple
from dataclasses import dataclass, field
from math import sin, pi, cos
from time import perf_counter
from typing import List, Callable

from pyglet.gl import *

import VertexRestrictions

Color = namedtuple("Color", "R, G, B")
Offset = namedtuple("Offset", "X, Y")

@dataclass(frozen = True)
class Config:
    Points: List[tuple]
    Proportion: float
    StartPoint: tuple
    StartPointColor: Color = Color(255, 255, 0)
    PlotPointColor: Color = Color(255, 255, 0)
    Iterations: int = 50_000
    VertexRestriction: Callable[[tuple, list], tuple] = field(default = VertexRestrictions.noRestriction)

# ----------------------------------------------------------------------------------------------------------

# support functions

def formatElapsedTime(val):
    if int(val) > 0:
        return f'{val:0.2f} seconds'
    else:
        val *= 1000
        if int(val) > 0:
            return f'{val:0.2f} milliseconds'
        else:
            val *= 1000
            if int(val) > 0:
                return f'{val:0.2f} microseconds'

    return f'{val:0.2f} nanoseconds'

def translate(p):
    w2 = int(width / 2)
    h2 = int(height / 2)
    x = p[0]
    y = p[1]

    if x > w2 or -x < -w2 or y > h2 or -y < -h2:
        raise ValueError

    x = w2 + x
    y = h2 - y

    return x, y

def makePoly(nVert, radius, proportion, startPoint, startPointColor = Color(255, 255, 0), plotPointColor = Color(255, 255, 0), offset = None, iterations = 50_000, vertexRestriction = VertexRestrictions.noRestriction):
    theta = (2 * pi) / nVert
    adj = pi / 4 if nVert == 4 else 0.0     # rotate square sides are vertical and horizontal
    ps = []

    for i in range(nVert):
        x = int(radius * sin(theta * i + adj))
        y = int(radius * cos(theta * i + adj))
        if offset is not None:
            x += offset.X
            y += offset.Y
        ps.append(translate((x, y)))

    return Config(ps, proportion, startPoint, startPointColor, plotPointColor, Iterations = iterations, VertexRestriction = vertexRestriction)

# ----------------------------------------------------------------------------------------------------------

# set up pygame

startTime = perf_counter()

width = 1200
height = width
title = "Chaos Game - Pyglet & OpenGL"

window = pyglet.window.Window(width, height, title)
window.set_location(800, 200)

# define a set of colors (used repeatedly as needed)

colors = [
    Color(255, 42, 42),         # red
    Color(17, 192, 16),         # green
    Color(55, 131, 255),        # blue
    Color(255, 140, 0),         # orange
    Color(124, 44, 255),        # magenta
    Color(57, 202, 187),        # cyan
    Color(238, 130, 238)        # pink
]

# define some patterns

sierpinski = makePoly(3, 650, 0.5, translate((0, 0)), startPointColor = Color(0, 0, 0), offset = Offset(0, -150), iterations = 100_000)
triangleSkewed = Config([translate((-500, -300)), translate((150, 400)), translate((500, -200))], 0.45, translate((0, 0)))
square = makePoly(4, 500, 0.45, translate((0, 0)))
fractalSquare = makePoly(4, 800, 0.5, translate((0, 0)), vertexRestriction = VertexRestrictions.avoidCurrent)
quadSkewed = Config([translate((-500, 300)), translate((400, 500)), translate((500, -450)), translate((-500, -500))], 0.4, translate((0, 0)))
diamond = Config([translate((-500, 0)), translate((0, 500)), translate((500, 0)), translate((0, -500))], 0.45, translate((0, 0)))
pentagon = makePoly(5, 500, 0.38, translate((0, 0)))
fractalPentagon = makePoly(5, 600, 0.5, translate((0, 0)), iterations = 100_000, vertexRestriction = VertexRestrictions.avoidCurrent)
hexagon = makePoly(6, 590, 0.33, translate((0, 0)))
fractalHexagon = makePoly(6, 590, 0.5, translate((0, 0)), iterations = 500_000, vertexRestriction = VertexRestrictions.avoidCurrent)
septagon = makePoly(7, 500, 0.31, translate((0, 0)))
octagon = makePoly(8, 500, 0.29, translate((0, 0)))
nonagon = makePoly(9, 500, 0.26, translate((0, 0)))
ring = makePoly(25, 500, 0.15, translate((0, 0)))
colorCheck = makePoly(len(colors), 100, 0.5, translate((0, 0)), iterations = 10, startPointColor = Color(0, 0, 0), plotPointColor = Color(0, 0, 0))

# select a pattern and create the layout

config = sierpinski
points = config.Points
startPoint = config.StartPoint
startPointcolor = config.StartPointColor
plotPointColor = config.PlotPointColor
prop = config.Proportion
numPoints = config.Iterations
restrictVertex = config.VertexRestriction
plotMarkerSize = 4
startPointSize = 2
point = None

@window.event
def on_draw():
    global numPoints, startPoint, plotPointColor, point

    glPointSize(8)

    glBegin(GL_POINTS)

    colorIdx = 0

    for i in range(len(points)):
        glColor3f(colors[colorIdx].R / 255, colors[colorIdx].G / 255, colors[colorIdx].B / 255)
        glVertex2f(points[i][0], height - points[i][1])
        colorIdx = (colorIdx + 1) % len(colors)

    glEnd()

    glPointSize(1)
    glColor3f(plotPointColor.R / 255, plotPointColor.G / 255, plotPointColor.B / 255)

    glBegin(GL_POINTS)

    for count in range(numPoints):
        point = restrictVertex(point, points)
        xDiff = int((point[0] - startPoint[0]) * (1.0 - prop))
        yDiff = int((point[1] - startPoint[1]) * (1.0 - prop))
        x = startPoint[0] + xDiff
        y = startPoint[1] + yDiff
        startPoint = (x, y)
        glVertex2f(x, height - y)

    glEnd()

    endTime = perf_counter()
    runTime = endTime - startTime
    print()
    print(f'{numPoints:,} points plotted in {formatElapsedTime(runTime)}')
    reported = True

pyglet.app.run()
