"""69,121-parameter candidate scorer, initialized from scratch and fitted to a teacher.
Synthetic supervision only; this is not reinforcement learning or a vision model.
"""
from pathlib import Path
import numpy as np
from .policy import FEATURES
PATH=Path(__file__).with_name('moderate.npz')
class NeuralPolicy:
    def __init__(self):
        self.w=np.load(PATH)
    def score(self,c):
        x=np.array([c.get('features',{}).get(k,0) for k in FEATURES],dtype=np.float32)
        return (np.maximum(0,np.maximum(0,x@self.w['w1']+self.w['b1'])@self.w['w2']+self.w['b2'])@self.w['w3']+self.w['b3']).item()
    def choose(self,cs):
        return max((c for c in cs if c.get('legal',True)),key=self.score,default={'action':'wait'})
def train():
    rng=np.random.default_rng(42)
    sizes=[len(FEATURES),256,256,1]
    weights={}
    for i,(a,b) in enumerate(zip(sizes,sizes[1:]),1):
        weights[f'w{i}']=(rng.normal(size=(a,b))*np.sqrt(2/a)).astype('float32')
        weights[f'b{i}']=np.zeros(b,dtype='float32')
    x=rng.uniform(0,1,(8192,len(FEATURES))).astype('float32');x*=rng.integers(0,2,x.shape);x[:,0]=0
    teacher=np.array([0,20,10,-60,-5,-6,35,-15,30,-.1,-100],dtype='float32')
    y=(x@teacher)[:,None]/100
    m={k:np.zeros_like(v) for k,v in weights.items()};v={k:np.zeros_like(v) for k,v in weights.items()}
    for t in range(1,3001):
        idx=rng.integers(0,len(x),128);a=x[idx]
        h=np.maximum(0,a@weights['w1']+weights['b1']);j=np.maximum(0,h@weights['w2']+weights['b2']);pred=j@weights['w3']+weights['b3']
        d=2*(pred-y[idx])/len(idx);g={'w3':j.T@d,'b3':d.sum(0)}
        e=(d@weights['w3'].T)*(j>0);g.update(w2=h.T@e,b2=e.sum(0))
        e=(e@weights['w2'].T)*(h>0);g.update(w1=a.T@e,b1=e.sum(0))
        for k in weights:
            m[k]=.9*m[k]+.1*g[k];v[k]=.999*v[k]+.001*g[k]**2
            weights[k]-=.001*(m[k]/(1-.9**t))/(np.sqrt(v[k]/(1-.999**t))+1e-8)
    np.savez(PATH,**weights)
    print({'parameters':sum(a.size for a in weights.values()),'training_mse':float(np.mean((pred-y[idx])**2))})
if __name__=='__main__':train()
