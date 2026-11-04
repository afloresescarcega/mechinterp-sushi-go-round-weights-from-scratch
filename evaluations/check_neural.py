"""Synthetic safety/ranking probes; live success is separately recorded."""
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sushi_policy.neural import NeuralPolicy
from sushi_policy.adapter import candidates
p=NeuralPolicy()
assert sum(p.w[k].size for k in p.w.files)==69121
wait={'action':'wait','features':{}}
for feature,action in [('orders_served','make'),('clears_seat','clear'),('refill_value','refill')]:
    c={'action':action,'features':{feature:1}}
    assert p.choose([wait,c])['action']==action
assert p.choose([wait,{'action':'make','legal':False,'features':{'orders_served':1}}])['action']=='wait'
for dish in ['onigiri','california','gunkan']:
    for stock,covered in [(0,False),(10,True)]:
        cs=candidates({'inventory':dict.fromkeys(['rice','nori','roe'],stock),'orders':[{'dish':dish,'covered':covered}]})
        assert p.choose(cs)['action']=='wait'
assert all(np.isfinite(p.w[k]).all() for k in p.w.files)
print('PASS: parameter count, finite weights, basic priorities, stock and duplicate legality')
