import numpy as np
from simulation.trafficSimulator import *
#from simulation.trafficSimulator.simulationAlgo import Simulation2

sim = Simulation()

# Play with these
n = 25
a = 2
b = 12
l = 100

# Nodes
WEST_RIGHT_START = (-b - l, a+a*2)
WEST_LEFT_START = (-b - l, -a)

SOUTH_RIGHT_START = (a, b + l)
SOUTH_MID_START = (-a, b + l)
SOUTH_LEFT_START = (-a-a*2, b + l)


EAST_RIGHT_START = (b + l, -a-a*2)
EAST_MID_START = (b + l, -a)
EAST_LEFT_START = (b + l, a+a*2)

NORTH_RIGHT_START = (-a-a*2, -b - l)
NORTH_MID_START = (-a, -b - l)
NORTH_LEFT_START = (a, -b - l)

WEST_RIGHT = (-b, a+a*2)
WEST_LEFT = (-b, -a)

SOUTH_RIGHT = (a, b)
SOUTH_MID = (-a, b)
SOUTH_LEFT = (-a-a*2, b)

EAST_RIGHT = (b, -a-a*2)
EAST_MID = (b, -a)
EAST_LEFT = (b, a+a*2)

NORTH_RIGHT = (-a-a*2, -b)
NORTH_MID = (-a, -b)
NORTH_LEFT = (a, -b)

# Roads
WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT,"Inbound")
SOUTH_INBOUND_RIGHT = (SOUTH_RIGHT_START, SOUTH_RIGHT,"Inbound")
SOUTH_INBOUND_MID = (SOUTH_MID_START, SOUTH_MID,"Inbound")
EAST_INBOUND_RIGHT = (EAST_RIGHT_START, EAST_RIGHT,"Inbound")
EAST_INBOUND_MID = (EAST_MID_START, EAST_MID,"Inbound")
NORTH_INBOUND_RIGHT = (NORTH_RIGHT_START, NORTH_RIGHT,"Inbound")
NORTH_INBOUND_MID = (NORTH_MID_START, NORTH_MID,"Inbound")

WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

WEST_STRAIGHT = (WEST_RIGHT, EAST_LEFT)
SOUTH_STRAIGHT = (SOUTH_RIGHT, NORTH_LEFT)
EAST_STRAIGHT = (EAST_MID, WEST_LEFT)
NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)

WEST_RIGHT_TURN = turn_road(WEST_RIGHT, SOUTH_LEFT, TURN_RIGHT, n)
WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)

SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT, EAST_LEFT, TURN_RIGHT, n)
SOUTH_LEFT_TURN = turn_road(SOUTH_MID, WEST_LEFT, TURN_LEFT, n)

EAST_RIGHT_TURN = turn_road(EAST_RIGHT, NORTH_LEFT, TURN_RIGHT, n)
EAST_LEFT_TURN = turn_road(EAST_MID, SOUTH_LEFT, TURN_LEFT, n)

NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT, WEST_LEFT, TURN_RIGHT, n)
NORTH_LEFT_TURN = turn_road(NORTH_MID, EAST_LEFT, TURN_LEFT, n)

sim.create_roads([
    WEST_INBOUND, #0
    SOUTH_INBOUND_RIGHT, #1
    SOUTH_INBOUND_MID, #2
    EAST_INBOUND_RIGHT, #3
    EAST_INBOUND_MID, #4
    NORTH_INBOUND_RIGHT, #5
    NORTH_INBOUND_MID, #6

    WEST_OUTBOUND, #7
    SOUTH_OUTBOUND, #8
    EAST_OUTBOUND, #9
    NORTH_OUTBOUND, #10

    WEST_STRAIGHT, #11
    SOUTH_STRAIGHT, #12
    EAST_STRAIGHT, #13
    NORTH_STRAIGHT, #14

    *WEST_RIGHT_TURN, #15
    *WEST_LEFT_TURN, #16

    *SOUTH_RIGHT_TURN, #17
    *SOUTH_LEFT_TURN, #18

    *EAST_RIGHT_TURN, #19
    *EAST_LEFT_TURN, #20

    *NORTH_RIGHT_TURN, #21
    *NORTH_LEFT_TURN #22
])


def road(a): return range(a, a + n)


sim.create_gen({
    'vehicle_rate': 5,
    'vehicles': [
       [1, {'path': [0, 11, 9]}],
       [1, {'path': [0, *road(15), 8]}],
       [1, {'path': [0, *road(15+n), 10]}],

       [1, {'path': [1, 12, 10]}],
       [1, {'path': [1, *road(15+2*n), 9]}],
       [1, {'path': [2, *road(15+3*n), 7]}],

        [1, {'path': [4, 13, 7]}],
        [1, {'path': [3, *road(15+4*n), 10]}],
        [1, {'path': [4, *road(15+5*n), 8]}],

        [1, {'path': [5, *road(15+6*n), 7]}],
        [1, {'path': [5, 14, 8]}],
        [1, {'path': [6, *road(15+7*n), 9]}],

    ]})

#parameters = {"cycle": [(True, False), (False, True)]}
sim.create_signal([[0]],config={'current_cycle_index':0,'identify':1,})
sim.create_signal([[1]],config={'current_cycle_index':1,'identify':2,'to_change':27})
sim.create_signal([[2]],config={'current_cycle_index':0,'identify':3})
sim.create_signal([[3]],config={'current_cycle_index':0,'identify':4})
sim.create_signal([[4]],config={'current_cycle_index':0,'identify':5})
sim.create_signal([[5]],config={'current_cycle_index':1,'identify':6,'to_change':27})
sim.create_signal([[6]],config={'current_cycle_index':0,'identify':7})
# Start simulation

win = Window(sim)
win.zoom = 10
win.run(steps_per_update=10)
