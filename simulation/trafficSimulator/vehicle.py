import numpy as np
import time


class Vehicle:
    def __init__(self, id, config={}):
        self.id = id
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        self.l = 4
        self.s0 = 4
        self.T = 1
        self.v_max = 2
        self.a_max = 1.44
        self.b_max = 4.61

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False
        self.stop_start = None
        self.stop_end = None
        self.totalStopTime = 0
        self.stoptime = None
        self.isstopped = False
        self.crossedsemaphor=False

    def init_properties(self):
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2

        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1 - (self.v / self.v_max) ** 4 - alpha ** 2)
        if self.stopped:
            self.a = -self.b_max * self.v / self.v_max
            if(self.isstopped==False):
                self.stoptime = time.time()
                self.isstopped=True
        else:
            if (self.stoptime != None):
                self.totalStopTime = self.totalStopTime + time.time() - self.stoptime
            self.isstopped=False
            self.stoptime = None
            self.stop_start = None

    def stop(self):
        self.stop_start = time.time()
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max

    def getStopTime(self):
        if self.stop_start != None:
            return self.stop_start - time.time()
        else:
            return 0

    def getTotalStopTime(self):
        return self.totalStopTime

    def countPrio(self,total_vehicles):
        time = self.getTotalStopTime()
        if time != None:
            prio = 1 + (time * time)/(total_vehicles*0.1)
        else:
            prio = 0
        return prio

