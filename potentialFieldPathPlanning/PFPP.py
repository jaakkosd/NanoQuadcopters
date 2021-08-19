import time
import csv
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils import uri_helper
import numpy as np
import sympy as sy
import controller as ctr

# URI to the Crazyflie to connect to
URI1 = 'radio://0/80/2M/E7E7E7E701'
URI2 = 'radio://0/80/2M/E7E7E7E703'

uris = {
    URI1,
    URI2,
}

#uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E701')
TOLERANCE = 0.15


class Position:

    def __init__(self, id):
        self.id = id
        self.current = np.array([[0], [0], [0]], dtype=float)
        self.goal = np.array([[0], [0], [1]], dtype=float)
        self.other = np.array([[0], [0], [0]], dtype=float)

    def give_current(self):
        return self.current[1]


def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            # print("{} {} {}".
            #       format(max_x - min_x, max_y - min_y, max_z - min_z))

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_position_estimator(cf)


def position_callback(timestamp, data, logconf):
    coordlist = []

    if logconf.name == "Position1":
        cf1Pos.current[0] = data['kalman.stateX']
        cf1Pos.other[0] = cf3Pos.current[0]
        x = float(cf1Pos.current[0])
        coordlist.append(x)

        cf1Pos.current[1] = data['kalman.stateY']
        cf1Pos.other[1] = cf3Pos.current[1]
        y = float(cf1Pos.current[1])
        coordlist.append(y)

        cf1Pos.current[2] = data['kalman.stateZ']

        with open('pos1.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(coordlist)

    if logconf.name == "Position3":
        cf3Pos.current[0] = data['kalman.stateX']
        cf3Pos.other[0] = cf1Pos.current[0]
        x = float(cf3Pos.current[0])
        coordlist.append(x)

        cf3Pos.current[1] = data['kalman.stateY']
        cf3Pos.other[1] = cf1Pos.current[1]
        y = float(cf3Pos.current[1])
        coordlist.append(y)

        cf3Pos.current[2] = data['kalman.stateZ']

        with open('pos3.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(coordlist)


    #print('pos: ({}, {}, {})'.format(cfPos.current[0], cfPos.current[1], cfPos.current[2]))
    #print('pos: {}'.format(cfPos.current[1]))


def start_position_printing(scf):
    if scf.cf.link_uri == URI1:
        log_conf = LogConfig(name='Position1', period_in_ms=50)
    else:
        log_conf = LogConfig(name='Position3', period_in_ms=51)
    log_conf.add_variable('kalman.stateX', 'float')
    log_conf.add_variable('kalman.stateY', 'float')
    log_conf.add_variable('kalman.stateZ', 'float')

    scf.cf.log.add_config(log_conf)
    log_conf.data_received_cb.add_callback(position_callback)
    log_conf.start()


if __name__ == '__main__':
    open('pos1.csv', 'w+')
    with open('pos1.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x1', 'y1'])

    open('pos3.csv', 'w+')
    with open('pos3.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x3', 'y3'])

    cflib.crtp.init_drivers()

    factory = CachedCfFactory(rw_cache='./cache')
    cf = Crazyflie(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel(reset_estimator)
        swarm.parallel(start_position_printing)
        cf1Pos = Position(1)
        cf3Pos = Position(3)
        seq_args = {
            URI1: [cf1Pos],
            URI2: [cf3Pos],
        }
        swarm.parallel(ctr.controller, args_dict=seq_args)
