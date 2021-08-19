import math
import numpy as np

r = 0.5
R = 1.0
constant = 0.125


def avController(cfPos, obstacle):

    u = np.array([[0], [0]], dtype=float)

    xc = cfPos.current[0]
    yc = cfPos.current[1]

    xo = obstacle[0]
    yo = obstacle[1]

    dist = math.sqrt(pow((xo - xc), 2) + pow((yo - yc), 2))  # Distance between agent and obstacle

    print(cfPos.id, ": ", dist)

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
