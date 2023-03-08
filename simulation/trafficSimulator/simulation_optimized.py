import time

from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .traffic_signal import TrafficSignal
import math

from ..stat.statistics import Statictics


class Simulation2:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()
        self.traffic_order = [[1,5],[3,6],[0],[4],[1,5],[2,3],[0]]
        self.traffic_time = [27,20,15,15,15,15,10]
        self.max_index = 0
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
        self.TotalStopTime = 0
        self.amountcarscrossed = 0
        self.simstarttime = time.time()
        self.stoptimestats = []
        self.allstats = []
        self.metricsdone = False

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
        if (time.time() - self.simstarttime > 60 and self.metricsdone == False):
            self.allstats.append(self.stoptimestats)
            Statictics().chartoptimalized(self.allstats)
            self.metricsdone = True
        # Update every road
        for road in self.roads:
            road.update(self.dt)
            if road.type == "Inbound":
                self.road_priority.append(self.countRoadPrio(road))
                vehicleCount = self.countVehicles(road)
                self.road_vehiclesGreenTime.append(self.countGreenTime(vehicleCount))

        # Add vehicles
        for gen in self.generators:
            gen.update()

        print(self.road_vehiclesGreenTime)

        # Update semaphores
        for index,sem in enumerate(self.traffic_signals):
            if sem.current_cycle_index:
                sem.update(self.road_vehiclesGreenTime[index])

        semaphor_not_running = all(sem.current_cycle_index == 0 for sem in self.traffic_signals)

        #Start semaphore if none is running
        if semaphor_not_running:
            self.max_index = self.choose_prio_road()

            for tr_light_index, node in enumerate(self.traffic_order):
                if self.max_index in node:
                    for semaphor in self.traffic_order[tr_light_index]:
                        self.traffic_signals[semaphor].current_cycle_index = 1
                    break

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
                    #print(self.throughput)
                    self.TotalStopTime = self.TotalStopTime + vehicle.getTotalStopTime()
                    vehicle.totalStopTime = 0
                    if (vehicle.crossedsemaphor == False):
                        self.amountcarscrossed += 1
                    vehicle.crossedsemaphor = True
                    if (self.amountcarscrossed != 0):
                        self.stoptimestats.append(
                            [str(time.time() - self.simstarttime), str(self.TotalStopTime / self.amountcarscrossed)])
                        # print(self.stoptimestats)
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

    def countVehiclePrio(self,vehicle,total):
        return vehicle.countPrio(total)

    def countRoadPrio(self,road):
        sum = 0
        for vehicle in road.vehicles:
            sum += self.countVehiclePrio(vehicle,len(road.vehicles))
        return sum
    def run(self, steps):
        for _ in range(steps):
            self.update()

    def countVehicles(self,road):
        return road.getVehiclesCount()

    def countGreenTime(self,vehicleCount):
        if vehicleCount == 1:
            return 4
        if vehicleCount > 7:
            vehicleCount = 7

        decay_rate = 0.4
        base = 4
        green_time = 0
        for i in range(vehicleCount):
            green_time += base * math.exp(-decay_rate*i)

        return green_time

    def update_troughput(self):
        self.throughput = len(self.cars_crossed) / self.t * 60

    def choose_prio_road(self):
        max_prio = max(self.road_priority)
        return self.road_priority.index(max_prio)
