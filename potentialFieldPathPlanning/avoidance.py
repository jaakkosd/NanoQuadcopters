import math
import numpy as np

r = 0.5
R = 1.0
constant = 0.25


def avController(cfPos, obstacle):

    u = np.array([[0], [0]], dtype=float)

    xc = cfPos.current[0]
    yc = cfPos.current[1]

    for obst in obstacle:
        xo = obst[0]
        yo = obst[1]

        dist = math.sqrt(pow((xo - xc), 2) + pow((yo - yc), 2))  # Distance between agent and obstacle

        if r < dist < R:

            uxtemp = -(4 * (pow(R, 2) - pow(r, 2)) * (pow(dist, 2) - pow(R, 2)) * (xc - xo)) / (
                pow(pow(dist, 2) - pow(r, 2), 3))

            uytemp = -(4 * (pow(R, 2) - pow(r, 2)) * (pow(dist, 2) - pow(R, 2)) * (yc - yo)) / (
                pow(pow(dist, 2) - pow(r, 2), 3))

            u[0] = uxtemp + u[0]
            u[1] = uytemp + u[1]

    if u[0] != 0 or u[1] != 0:
        Ka = constant / (math.sqrt(pow(u[0], 2) + pow(u[1], 2)))
        u = Ka * u
        return u

    else:
        return u
