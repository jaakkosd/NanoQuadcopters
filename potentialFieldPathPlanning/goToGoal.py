
Kg = 0.025


def goToGoal(cfPos):

    xc = cfPos.current[0]
    yc = cfPos.current[1]
    zc = cfPos.current[2]

    xg = cfPos.goal[0]
    yg = cfPos.goal[1]
    zg = cfPos.goal[2]

    ux = (-2 * (xc - xg)) * Kg  # Neg gradient of the pot. function * P-gain

    uy = (-2 * (yc - yg)) * Kg  # Neg gradient of the pot. function * P-gain

    uz = (-2 * (zc - zg)) * Kg

    return [ux, uy, uz]
