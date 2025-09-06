import json, random
from core.simulation_base import SimulationBase


class MarketingSimulator(SimulationBase):
    def __init__(self, scenario_path: str):
        with open(scenario_path) as f:
            self.scenario_data = json.load(f)
            self.state_template = self.scenario_data['metadata']['initial_metrics']


    def new_session(self, user_id='anon'):
        session = {
            'user_id': user_id,
            'metrics': self.state_template.copy(),
            'history': [],
            'metrics_history': [self.state_template.copy()]
        }
        return session


    def apply_decision(self, session, decision_id, option_id):
        metrics = session['metrics']
        if decision_id == 'alloc_budget':
            if option_id == 'yes_shift':
                metrics['budget_share_top_channel'] = max(0, metrics['budget_share_top_channel'] - 0.1)
                metrics['ctr'] += random.uniform(0.001, 0.003)
                metrics['conversion_rate'] += random.uniform(0.001, 0.004)
            elif option_id == 'no_shift':
                metrics['ctr'] += random.uniform(-0.001, 0.001)
        elif decision_id == 'change_creative':
            if option_id == 'run_ab':
                metrics['ctr'] += random.uniform(0.002, 0.005)
                metrics['conversion_rate'] += random.uniform(0.002, 0.004)
        session['history'].append({'decision_id': decision_id, 'option_id': option_id, 'metrics': metrics.copy()})
        session['metrics_history'].append(metrics.copy())


    def evaluate_session(self, session):
        metrics = session['metrics']
        advice = {}
        if metrics.get('budget_share_top_channel',0) > 0.8:
            advice['diversify_budget'] = 'Consider diversifying your budget to avoid diminishing returns.'
        if metrics.get('ctr',0) < self.scenario_data['metadata'].get('ctr_benchmark',0.05):
            advice['improve_creatives'] = 'CTR below benchmark — consider creative improvements.'
        if metrics.get('conversion_rate',0) < self.scenario_data['metadata'].get('conv_benchmark',0.03):
            advice['optimize_landing'] = 'Conversion rate below benchmark — optimize landing page.'
        return {'metrics': metrics, 'advice': advice, 'history': session['history']}