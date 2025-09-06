import json, random
from core.simulation_base import SimulationBase


class OutbreakSimulator(SimulationBase):
    def __init__(self, scenario_path):
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
        if decision_id == 'enforce_quarantine':
            if option_id == 'yes_quarantine':
                metrics['infected'] = max(0, metrics['infected'] - random.randint(1,5))
                metrics['contained'] += 1
            else:
                metrics['infected'] += random.randint(5,10)
        session['history'].append({'decision_id': decision_id,'option_id': option_id,'metrics': metrics.copy()})
        session['metrics_history'].append(metrics.copy())


    def evaluate_session(self, session):
        metrics = session['metrics']
        advice = {}
        if metrics.get('infected',0) > 50:
            advice['implement_quarantine'] = 'High infection numbers — implement containment.'
        return {'metrics': metrics, 'advice': advice, 'history': session['history']}