import random

from artemis.src.core.simulation_config import SimulationConfig


class ArtemisModel:
    def __init__(self, simulationConfig:SimulationConfig):
        self.simulationConfig = simulationConfig
        random.seed(simulationConfig.seed)

    def get_random_int(self)->int:
        return random.randint(0, 100)

    def get_random_float(self)->float:
        return random.random()
