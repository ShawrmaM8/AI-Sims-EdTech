import json, random
from core.simulation_base import SimulationBase


class ChronicCareSimulator(SimulationBase):
    def __init__(self, scenario_path):
        with open(scenario_path) as f:
            self.scenario_data = json.load(f)