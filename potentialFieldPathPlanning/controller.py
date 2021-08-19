import time
import math
import sympy as sy
import numpy as np
import avoidance as avc
import goToGoal as gtg

TOLERANCE = 0.15
Kp = 0.1


def ask_goal_pos(cfPos):
    print(" Current position is: ", '({}, {}, {})'.format(cfPos.current[0], cfPos.current[1], cfPos.current[2]))
    goalpos = input("Give the goal x-coordinate :")
    cfPos.goal[0] = goalpos

    goalpos = input("Give the goal y-coordinate :")
    cfPos.goal[1] = goalpos

    goalpos = input("Give the goal z-coordinate :")
    #cfPos.goal[2] = goalpos


def take_off(cf, height):
    take_off_time = 1.0
    sleep_time = 0.1
    steps = int(take_off_time / sleep_time)
    vz = height / take_off_time

    for i in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)


def is_in_goal(cfPos):
    xc = cfPos.current[0]
    yc = cfPos.current[1]

    xg = cfPos.goal[0]
    yg = cfPos.goal[1]

    dist = math.sqrt(pow((xg - xc), 2) + pow((yg - yc), 2))  # Distance between agent and goal
    if dist < TOLERANCE:
        return True
    else:
        return False


def controller(scf, cfPos):
    cf = scf.cf
    time.sleep(0.2)

    ask_goal_pos(cfPos)

    take_off(cf, 0.5)

    in_goal = False

    while not in_goal:
        ug = gtg.goToGoal(cfPos)  # GoToGoal controls

        ugx = ug[0]
        ugy = ug[1]
        ugz = ug[2]

        print("gotogoal", ugx, ugy)

        ua = avc.avController(cfPos, [[0, 0], [0.5, 0.8]])  # Calculate avoidance controls

        uax = ua[0]
        uay = ua[1]

        print("avoidance :", uax, uay)

        # Add goal to goal control to collision avoidance control
        ux = ugx + uax
        uy = ugy + uay
        uz = ugz


        print("control u: ", ux, uy, uz)

        cf.commander.send_velocity_world_setpoint(ux, uy, uz, 0)
        print("pos: ", cfPos.current[0], cfPos.current[1], cfPos.current[2])

        in_goal = is_in_goal(cfPos)
        time.sleep(0.1)

    cf.commander.send_stop_setpoint()

    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)
