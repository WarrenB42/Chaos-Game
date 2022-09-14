import random
from collections import namedtuple
from dataclasses import dataclass
from math import sin, pi, cos
from time import perf_counter
from typing import List

import pygame

Color = namedtuple("Color", "R, G, B")

@dataclass(frozen = True)
class Config:
    Points: List[tuple]
    Proportion: float
    StartPoint: tuple
    StartPointColor: Color

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

def makePoly(nVert, radius, proportion, startPoint, startPointColor):
    theta = (2 * pi) / nVert
    adj = pi / 4 if nVert == 4 else 0.0     # rotate square sides are vertical and horizontal
    ps = []

    for i in range(nVert):
        x = int(radius * sin(theta * i + adj))
        y = int(radius * cos(theta * i + adj))
        ps.append(translate((x, y)))

    return Config(ps, proportion, startPoint, startPointColor)

# ----------------------------------------------------------------------------------------------------------

# set up pygame

startTime = perf_counter()

width = 1200
height = width

win = pygame.display
win.set_caption("PyGame Chaos Game")
winSurface = pygame.HWSURFACE | pygame.DOUBLEBUF

display = win.set_mode((width, height))
canvas = pygame.Surface((width, height))

# define a set of colors (used repeatedly as needed)

colors = [
    Color(255, 42, 42),
    Color(17, 192, 16),
    Color(55, 131, 255),
    Color(255, 140, 0),
    Color(124, 44, 255),
    Color(57, 202, 187),
    Color(238, 130, 238)
]

# define some patterns

sierpinski = makePoly(3, 550, 0.5, translate((0, 0)), Color(255, 255, 0))
triangleSkewed = Config([translate((-500, -500)), translate((150, 200)), translate((500, -400))], 0.45, translate((0, 0)), Color(255, 255, 0))
square = makePoly(4, 500, 0.45, translate((0, 0)), Color(255, 255, 0))
quadSkewed = Config([translate((-500, 300)), translate((400, 500)), translate((500, -450)), translate((-500, -500))], 0.4, translate((0, 0)), Color(255, 255, 0))
diamond = Config([translate((-500, 0)), translate((0, 500)), translate((500, 0)), translate((0, -500))], 0.45, translate((0, 0)), Color(255, 255, 0))
pentagon = makePoly(5, 500, 0.38, translate((0, 0)), Color(255, 255, 0))
hexagon = makePoly(6, 500, 0.33, translate((0, 0)), Color(255, 255, 0))
septagon = makePoly(7, 500, 0.31, translate((0, 0)), Color(255, 255, 0))
octagon = makePoly(8, 500, 0.29, translate((0, 0)), Color(255, 255, 0))
nonagon = makePoly(9, 500, 0.26, translate((0, 0)), Color(255, 255, 0))
ring = makePoly(25, 500, 0.15, translate((0, 0)), Color(255, 255, 0))

# select a pattern and create the layout

config = square
points = config.Points
startPoint = config.StartPoint
color = config.StartPointColor
prop = config.Proportion
plotMarkerSize = 4
startPointSize = 2

colorIdx = 0
for i in range(len(points)):
    pygame.draw.circle(canvas, colors[colorIdx], points[i], plotMarkerSize)
    colorIdx = (colorIdx + 1) % len(colors)

# display the layout

pygame.draw.circle(canvas, color, startPoint, startPointSize)

win.flip()

# set up the drawing and run the pygame loop

numPoints = 50_000
count = 0
dispInterval = 10
run = True
reported = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    # add a point

    if count < numPoints:
        v = random.choice(points)
        xDiff = int((v[0] - startPoint[0]) * (1.0 - prop))
        yDiff = int((v[1] - startPoint[1]) * (1.0 - prop))
        x = startPoint[0] + xDiff
        y = startPoint[1] + yDiff
        startPoint = (x, y)
        canvas.set_at((x, y), color)
        count += 1
        # display points at a redued rate that is visible with good performance
        if count % dispInterval == 0:
            display.blit(canvas, (0, 0))
            win.flip()
    else:
        if not reported:
            endTime = perf_counter()
            runTime = endTime - startTime
            print()
            print(f'{numPoints:,} points plotted in {formatElapsedTime(runTime)}')
            reported = True

pygame.quit()
