import json, random
from core.simulation_base import SimulationBase


class HRConflictSimulator(SimulationBase):
    def __init__(self, scenario_path: str):
        with open(scenario_path) as f:
            self.scenario_data = json.load(f)


def new_session(self, user_id='anon'):
    session = {
        'user_id': user_id,
        'metrics': self.scenario_data['metadata']['initial_metrics'].copy(),
        'history': [],
        'metrics_history': [self.scenario_data['metadata']['initial_metrics'].copy()]
    }
    return session


def apply_decision(self, session, decision_id, option_id):
    metrics = session['metrics']
    if decision_id == 'mediate_conflict':
        if option_id == 'yes_mediate':
            metrics['stress_level'] = max(0, metrics['stress_level'] - random.randint(1,3))
        else:
            metrics['stress_level'] += random.randint(1,2)
    session['history'].append({'decision_id': decision_id, 'option_id': option_id, 'metrics': metrics.copy()})
    session['metrics_history'].append(metrics.copy())


def evaluate_session(self, session):
    metrics = session['metrics']
    advice = {}
    if metrics.get('stress_level',0) > self.scenario_data['metadata'].get('stress_threshold',5):
        advice['reduce_stress'] = 'High stress detected — consider mediation or role adjustment.'
    return {'metrics': metrics, 'advice': advice, 'history': session['history']}