"""Hand-authored linear action ranker. No training, external libraries, or game cheats.

Perception must supply visible facts and legal action candidates. This module does
not claim to recognize screenshots or control the CrazyGames browser.
"""
import json
from pathlib import Path

FEATURES = ('bias', 'orders_served', 'urgency', 'already_on_belt',
            'waste', 'stockout_risk', 'refill_value', 'cost_fraction',
            'clears_seat', 'action_seconds', 'unaffordable')

class Policy:
    def __init__(self, weights=None):
        path = Path(weights) if weights else Path(__file__).with_name('weights.json')
        self.weights = json.loads(path.read_text())
        if set(self.weights) != set(FEATURES):
            raise ValueError('Weights must match the documented feature schema')

    def score(self, candidate):
        unknown = set(candidate.get('features', {})) - set(FEATURES)
        if unknown:
            raise ValueError(f'Unknown features: {unknown}')
        return sum(self.weights[k] * candidate.get('features', {}).get(k, 0.0)
                   for k in FEATURES)

    def choose(self, candidates):
        legal = [c for c in candidates if c.get('legal', True)]
        if not legal:
            return {'action': 'wait', 'features': {}}
        return max(legal, key=self.score)

if __name__ == '__main__':
    import sys
    policy = Policy(sys.argv[1] if len(sys.argv) > 1 else None)
    for line in sys.stdin:
        state = json.loads(line)
        print(json.dumps(policy.choose(state['candidates'])), flush=True)
