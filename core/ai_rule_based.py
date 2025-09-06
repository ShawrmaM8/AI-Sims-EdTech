# core/ai_rule_based.py
from typing import Dict


# Small collection of rule-based helpers used by the marketing sim and others.

def apply_marketing_rules(metrics: Dict[str, float], scenario_meta: Dict) -> Dict[str, str]:
"""Return advice strings keyed by tag. metrics is mutable copy of current metrics."""
    advice = {}
    budget_share = metrics.get('budget_share_top_channel', 0.0)
    ctr = metrics.get('ctr', 0.0)
    conversion = metrics.get('conversion_rate', 0.0)


if budget_share > 0.8:
    advice['diversify_budget'] = ('High concentration of spend on one channel detected. ', 'Consider shifting up to 20% to other channels to avoid diminishing returns.')
    if ctr < scenario_meta.get('ctr_benchmark', 0.02):
        advice['improve_creatives'] = 'CTR below benchmark — run A/B tests on creative and call-to-action.'
    if conversion < scenario_meta.get('conv_benchmark', 0.02):
        advice['optimize_landing'] = 'Conversion rate below benchmark — optimize landing page and offer.'


    return advice