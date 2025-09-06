from abc import ABC, abstractmethod


class SimulationBase(ABC):
    @abstractmethod
    def __init__(self, scenario_path: str):
        pass


    @abstractmethod
    def new_session(self, user_id: str):
        pass


    @abstractmethod
    def apply_decision(self, session, decision_id: str, option_id: str):
        pass


    @abstractmethod
    def evaluate_session(self, session):
        pass