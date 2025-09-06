import json
from core.simulation_base import SimulationBase


class PharmacologySimulator(SimulationBase):
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
        if decision_id == 'administer_med':
            if option_id == 'wrong_dose':
                metrics['med_error'] += 1
        session['history'].append({'decision_id': decision_id,'option_id': option_id,'metrics': metrics.copy()})
        session['metrics_history'].append(metrics.copy())


    def evaluate_session(self, session):
        metrics = session['metrics']
        advice = {}
        if metrics.get('med_error',0) > 0:
            advice['check_med'] = 'Medication error detected — review dosages.'
        return {'metrics': metrics, 'advice': advice, 'history': session['history']}