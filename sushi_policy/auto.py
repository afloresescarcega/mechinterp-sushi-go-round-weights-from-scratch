"""One screenshot -> one policy decision; transport executes returned clicks."""
import json,sys,time
from pathlib import Path
from .vision import observe
from .adapter import candidates,RECIPES
from .policy import Policy
p=Path('evaluations/auto-state.json')
s=json.loads(p.read_text()) if p.exists() else {'inventory':{'rice':10,'nori':10,'roe':10},'pending':[],'deliveries':[],'made':0}
now=time.time()
for delivery in s['deliveries'][:]:
    if now>delivery['at']:
        s['inventory'][delivery['item']]+=10;s['deliveries'].remove(delivery)
s['pending']=[x for x in s['pending'] if now-x['at']<90]
o=observe(sys.argv[1]);o['inventory']=s['inventory'].copy()
for prev in s.get('previous_orders',[]):
    if not any(x['seat']==prev['seat'] and x['dish']==prev['dish'] for x in o['orders']):
        for pending in s['pending']:
            if pending['dish']==prev['dish']:
                s['pending'].remove(pending);break
s['previous_orders']=o['orders']
counts={d:sum(x['dish']==d for x in s['pending']) for d in RECIPES}
for order in sorted(o['orders'],key=lambda x:x['seat']):
    d=order['dish'];order['covered']=int(counts[d]>0);counts[d]=max(0,counts[d]-1)
o['refills']={}
for item,cost,menu in [('roe',200,[[687,315],[719,320]]),('rice',100,[[687,333],[692,324]]),('nori',100,[[687,315],[647,320]])]:
    if s['inventory'][item]<max([RECIPES[x['dish']].get(item,0) for x in o['orders'] if not x['covered']]+[0]) and s['made']>=3 and not any(x['item']==item for x in s['deliveries']):
        o['refills'][item]={'value':1,'cost_fraction':1.0 if o['closing'] else 0.3,'clicks':[[725,395]]+menu+[[648,335]]}
decision=Policy().choose(candidates(o))
if decision['action']=='make':
    d=decision['dish']
    for k,v in RECIPES[d].items():s['inventory'][k]-=v
    s['pending'].append({'dish':d,'at':now});s['made']+=1
elif decision['action']=='refill':s['deliveries'].append({'item':decision['item'],'at':now+7})
p.write_text(json.dumps(s))
with open('evaluations/auto-decisions.jsonl','a') as f:f.write(json.dumps({'time':now,'observation':o,'decision':decision})+'\n')
print(json.dumps(decision))
