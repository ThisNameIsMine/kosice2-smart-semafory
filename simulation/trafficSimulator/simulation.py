import time

from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .traffic_signal import TrafficSignal
from array import *
import math

from ..stat.statistics import Statictics


class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()
        self.traffic_order = [[1,5],[3,6],[0],[4],[1,5],[2,3],[0]]
        self.traffic_time = [27,20,15,15,15,15,10]
        self.state = 0
        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)


    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60          # Simulation time step
        self.roads = []         # Array to store roads
        self.generators = []
        self.traffic_signals = []
        self.road_priority = []
        self.road_vehiclesGreenTime = []
        self.cars_spawned = 0
        self.cars_crossed = set()
        self.throughput = 0
        self.TotalStopTime=0
        self.amountcarscrossed=0
        self.simstarttime=time.time()
        self.stoptimestats=[]
        self.allstats=[]
        self.metricsdone=False

    def create_road(self, start, end,type=None):
        road = Road(start, end,type)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)


    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        return gen

    def create_signal(self, roads, config={}):
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        sig = TrafficSignal(roads, config)
        self.traffic_signals.append(sig)
        return sig

    def update(self):
        # Update every road
        if(time.time()-self.simstarttime>60 and self.metricsdone==False):
            self.allstats.append(self.stoptimestats)
            Statictics().chartoriginal(self.allstats)
            self.metricsdone=True
        for road in self.roads:
            road.update(self.dt)
            if road.type == "Inbound":
                self.road_priority.append(self.countRoadPrio(road))
                vehicleCount = self.countVehicles(road)
                self.road_vehiclesGreenTime.append(self.countGreenTime(vehicleCount))
                #print(self.road_vehiclesGreenTime)
        # Add vehicles
        for gen in self.generators:
            gen.update()
        '''
        for signal in self.traffic_signals:
            if signal.current_cycle_index == 1:
                signal.update(self)
        '''
        '''
        for i in range(len(self.traffic_order)):
            for j in range((len(self.traffic_order[i]))):
                #self.traffic_order[i].update()
                if self.traffic_signals[self.traffic_order[i][j]].current_cycle_index == 1:
                    self.traffic_signals[self.traffic_order[i][j]].update(self.traffic_time[i])
                    if self.traffic_signals[self.traffic_order[i][j]].current_cycle_index == 0:
                        if i < len(self.traffic_order)-1:
                            #TODO choose next - i+1[all]
                            for h in range(len(self.traffic_order[i+1])):
                                self.traffic_signals[self.traffic_order[i + 1][h]].current_cycle_index = 1
                        else:
                            self.traffic_signals[self.traffic_order[0][0]].current_cycle_index = 1
                            self.traffic_signals[self.traffic_order[0][1]].current_cycle_index = 1
        '''
        #print(f'state {self.state}')
        if self.state == 0:
            for h in range(len(self.traffic_order[0])):
                self.traffic_signals[self.traffic_order[0][h]].update(self.traffic_time[self.state])

            if self.traffic_signals[self.traffic_order[0][0]].current_cycle_index == 0 or self.traffic_signals[self.traffic_order[0][1]].current_cycle_index == 0 :

                self.traffic_signals[self.traffic_order[0][0]].current_cycle_index = 0
                self.traffic_signals[self.traffic_order[0][1]].current_cycle_index = 0
                self.state = 1
        elif self.state == 1:#self.traffic_order = [[1,5],[3,6],[0],[4],[1,5],[2,3],[0]]
            for h in range(len(self.traffic_order[self.state])):
                self.traffic_signals[self.traffic_order[self.state][h]].update(self.traffic_time[self.state])

            if self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index == 0:
                self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index = 0
                self.traffic_signals[self.traffic_order[self.state][1]].current_cycle_index = 0
                self.state = 2

        elif self.state == 2:#self.traffic_order = [[1,5],[3,6],[0],[4],[1,5],[2,3],[0]]
            for h in range(len(self.traffic_order[self.state])):
                self.traffic_signals[self.traffic_order[self.state][h]].update(self.traffic_time[self.state])

            if self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index == 0:

                self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index = 0
                self.state = 3

        elif self.state == 3:#self.traffic_order = [[1,5],[3,6],[0],[4],[1,5],[2,3],[0]]
            for h in range(len(self.traffic_order[self.state])):
                self.traffic_signals[self.traffic_order[self.state][h]].update(self.traffic_time[self.state])

            if self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index == 0:

                self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index = 0
                self.state = 4
        elif self.state == 4:#self.traffic_order = [[1,5],[3,6],[0],[4],[1,5],[2,3],[0]]
            for h in range(len(self.traffic_order[self.state])):
                self.traffic_signals[self.traffic_order[self.state][h]].update(self.traffic_time[self.state])

            if self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index == 0:

                self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index = 0
                self.traffic_signals[self.traffic_order[self.state][1]].current_cycle_index = 0
                self.state = 5

        elif self.state == 5:#self.traffic_order = [[1,5],[3,6],[0],[4],[1,5],[2,3],[0]]
            for h in range(len(self.traffic_order[self.state])):
                self.traffic_signals[self.traffic_order[self.state][h]].update(self.traffic_time[self.state])

            if self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index == 0:

                self.traffic_signals[self.traffic_order[self.state][0]].current_cycle_index = 0
                self.state = 1

        #ifland
        #if self.traffic_signals[self.traffic_order[i][j]].current_cycle_index == 1:


        """for i in range(len(self.traffic_signals)):
            if self.traffic_signals[i].current_cycle_index == 1:
                #print(f'index {i}')
                self.traffic_signals[i].update(self)

                if self.traffic_signals[i].current_cycle_index == 0:

                    if i != len(self.traffic_signals)-1:
                        sd = len(self.traffic_signals)
                        #print(f'index {sd}')
                        self.traffic_signals[i+1].current_cycle_index = 1
                    else:
                        #print('here')
                        self.traffic_signals[0].current_cycle_index = 1
        """


        # Check roads for out of bounds vehicle
        for road in self.roads:
            # If road has no vehicles, continue
            if len(road.vehicles) == 0: continue
            # If not
            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length:
                #Checks if car has crossed road before if not,
                # will add car to cars that crossed road
                if vehicle.id not in self.cars_crossed:
                    self.cars_crossed.add(vehicle.id)
                    self.update_troughput()
                    self.TotalStopTime=self.TotalStopTime+vehicle.getTotalStopTime()
                    vehicle.totalStopTime=0
                    if(vehicle.crossedsemaphor==False):
                        self.amountcarscrossed+=1
                    vehicle.crossedsemaphor=True
                    if(self.amountcarscrossed!=0):
                        self.stoptimestats.append([str(time.time()-self.simstarttime),str(self.TotalStopTime/self.amountcarscrossed)])
                        #print(self.stoptimestats)


                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):

                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Create a copy and reset some vehicle properties
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                # In all cases, remove it from its road
                road.vehicles.popleft()

        # Increment time
        self.t += self.dt
        self.frame_count += 1
        self.road_priority = []
        self.road_vehiclesGreenTime = []





    def countRoadPrio(self,road):
        sum = 0
        for vehicle in road.vehicles:
            sum += 0
        return sum
    def run(self, steps):
        for _ in range(steps):
            self.update()

    def countVehicles(self,road):
        return road.getVehiclesCount()

    def countGreenTime(self,vehicleCount):
        car_length = 4
        gap_length = 2
        car_acc = 4
        greenTime = 0
        for i in range(vehicleCount-1):
            s = i*car_length+(i+1)*gap_length
            t = math.sqrt(2*s-car_acc)
            for j in range(i):
                if t > 1:
                    t = math.log(t)
            greenTime += t
        return greenTime

    def update_troughput(self):
        self.throughput = len(self.cars_crossed) / self.t * 60

