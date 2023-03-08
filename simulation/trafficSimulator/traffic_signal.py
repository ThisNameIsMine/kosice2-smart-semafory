class TrafficSignal:
    def __init__(self, roads, config={}):
        # Initialize roads
        self.roads = roads
        # Set default configuration
        self.set_default_config()
        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)
        # Calculate properties
        self.init_properties()
        self.tochange = 0
        self.senzor = False
        self.identify = 0
        self.first = True

    # zakladne nastavenie semaforov - list vsetkych traffic lights, 1 ako zacne 2 naco sa meni
    def set_default_config(self):
        self.cycle = [(False, True), (True, False)]
        self.slow_distance = 50
        self.slow_factor = 0.4
        self.stop_distance = 15

        self.current_cycle_index = 0

        self.last_t = 0

    def init_properties(self):
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)

    @property
    def current_cycle(self):
        #print(self.cycle[self.current_cycle_index])
        return self.cycle[self.current_cycle_index]
    
    def update(self, set_time):
        if self.first:
            self.tochange = set_time*100
            self.current_cycle_index = 1
            self.first = False

        else:
            if self.current_cycle_index:
                self.tochange -= 1
                #print(f'change {self.tochange}')
                if self.tochange <= 0:
                    self.first = True
                    self.current_cycle_index = 0





