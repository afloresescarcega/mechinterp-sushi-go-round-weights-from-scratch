"""Visible-state adapter. Receives manually transcribed screenshot observations.
Coordinates are calibrated for the 1280x800 CrazyGames page, not arbitrary windows.
"""
import json
import sys
from pathlib import Path
from .policy import Policy
RECIPES = {'onigiri': {'rice':2,'nori':1}, 'california':{'rice':1,'nori':1,'roe':1},
           'gunkan':{'rice':1,'nori':1,'roe':2}}
POINTS = {'rice':[295,369], 'nori':[247,418], 'roe':[295,418], 'roll':[390,414]}

def candidates(state):
    cs = [{'action':'wait', 'features':{}}]
    for order in state.get('orders',[]):
        recipe = RECIPES[order['dish']]
        legal = all(state['inventory'].get(k,0)>=v for k,v in recipe.items())
        cs.append({'action':'make','dish':order['dish'],'legal':legal,
          'clicks':[POINTS[k] for k,v in recipe.items() for _ in range(v)]+[POINTS['roll']],
          'features':{'orders_served':1,'urgency':order.get('urgency',0),
                      'already_on_belt':order.get('covered',0),'action_seconds':1}})
    for seat in state.get('plates',[]):
        cs.append({'action':'clear','seat':seat,'clicks':[[[286,375,463,552,640,728][seat],257]],
                   'features':{'clears_seat':1,'action_seconds':0.2}})
    for item, info in state.get('refills', {}).items():
        cs.append({'action':'refill','item':item,'legal':info.get('legal',True),
                   'features':{'refill_value':info['value'],'cost_fraction':info['cost_fraction']},
                   'clicks':info['clicks']})
    return cs

if __name__ == '__main__':
    state = json.load(sys.stdin)
    decision = Policy().choose(candidates(state))
    log = Path('evaluations/live-decisions.jsonl')
    with log.open('a') as f:
        f.write(json.dumps({'observation':state,'decision':decision})+'\n')
    print(json.dumps(decision))
