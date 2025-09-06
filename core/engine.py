# core/engine.py
import json
from typing import Dict, Any
from core.entities import Scenario, Actor, Decision, DecisionOption, Outcome


def load_scenario_from_json(path: str) -> Scenario:
    with open(path, 'r') as f:
        payload = json.load(f)


    actors = [Actor(a['id'], a.get('role', ''), a.get('attributes', {})) for a in payload.get('actors', [])]


    decisions = []
    for d in payload.get('decisions', []):
        options = [DecisionOption(o['id'], o['label'], o['outcome_id']) for o in d.get('options', [])]
        decisions.append(Decision(d['id'], d['prompt'], options))


    outcomes = [Outcome(o['id'], o['description'], o.get('impact', {}), o.get('feedback', '')) for o in payload.get('outcomes', [])]


    scen = Scenario(payload['id'], payload['title'], payload.get('description', ''), actors, decisions, outcomes, payload.get('metadata', {}))
    return scen




class RuntimeSession:
    """Holds session state while a user runs through a scenario."""
    def __init__(self, scenario: Scenario, user_id: str = 'anon'):
        self.scenario = scenario
        self.user_id = user_id
        self.state = {
            'metrics': {k: v for k, v in (scenario.metadata.get('initial_metrics') or {}).items()},
            'history': [] # list of (decision_id, option_id, outcome_id)
        }


def apply_decision(self, decision_id: str, option_id: str) -> Outcome:
    d = self.scenario.get_decision(decision_id)
    opt = None
    for o in d.options:
        if o.id == option_id:
            opt = o
            break
        if opt is None:
            raise KeyError(f"Option {option_id} not found for decision {decision_id}")

    outcome = self.scenario.get_outcome(opt.outcome_id)

    # apply numeric impacts
    for metric, delta in outcome.impact.items():
        self.state['metrics'][metric] = self.state['metrics'].get(metric, 0.0) + delta
    self.state['history'].append({'decision_id': decision_id, 'option_id': option_id, 'outcome_id': outcome.id})
    return outcome