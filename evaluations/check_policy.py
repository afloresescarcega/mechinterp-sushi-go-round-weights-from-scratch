"""Deterministic decision probes, NOT a game simulator or Day 1 evaluation."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sushi_policy.policy import Policy

CASES = [
 ('serve_order', [{'action':'make','features':{'orders_served':1}}, {'action':'wait','features':{}}], 'make'),
 ('avoid_duplicate', [{'action':'make','features':{'orders_served':1,'already_on_belt':1}}, {'action':'wait','features':{}}], 'wait'),
 ('clear_seat', [{'action':'clear','features':{'clears_seat':1}}, {'action':'wait','features':{}}], 'clear'),
 ('urgent_order_before_clear', [{'action':'make','features':{'orders_served':1,'urgency':1}}, {'action':'clear','features':{'clears_seat':1}}], 'make'),
 ('avoid_unaffordable', [{'action':'buy','legal':False,'features':{'refill_value':1}}, {'action':'wait','features':{}}], 'wait'),
]
results = {}
for version in ('weights.v0.json','weights.json'):
    p = Policy(Path(__file__).resolve().parents[1] / 'sushi_policy' / version)
    results[version] = [{'probe':name,'expected':expected,'actual':p.choose(cs)['action'],
                         'passed':p.choose(cs)['action']==expected} for name, cs, expected in CASES]
print(json.dumps({'kind':'synthetic_decision_probes','real_game_evaluated':False,'results':results},indent=2))
assert all(r['passed'] for r in results['weights.json'])
