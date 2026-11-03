"""Hand-coded color features for the fixed 1280x800 viewport. No fitted weights."""
from PIL import Image
X = [265,354,442,531,619,707]
def observe(path):
    im=Image.open(path).convert('RGB')
    orders=[];plates=[]
    for seat,x in enumerate(X):
        pixels=[im.getpixel((a,b)) for a in range(x-10,x+10) for b in range(123,149)]
        black=sum(max(p)<75 for p in pixels)
        orange=sum(p[0]>170 and 65<p[1]<210 and p[2]<90 for p in pixels)
        white=sum(min(p)>210 for p in pixels)
        if black>35 and white>30:
            dish='gunkan' if orange>15 and black>100 else ('california' if orange>2 else 'onigiri')
            red=sum(1 for a in range(x-15,x+23) if (lambda p:p[0]>130 and p[0]>p[1]*1.4)(im.getpixel((a,172))))
            orders.append({'seat':seat,'dish':dish,'urgency':max(0,1-red/25), 'counts':[black,orange,white]})
        r,g,b=im.getpixel(([286,375,463,552,640,728][seat],257))
        if r>200 and 80<g<200 and b>120:
            plates.append(seat)
    belt=[]
    runs=[];start=None
    for x in range(216,776):
        r,g,b=im.getpixel((x,300));pink=r>200 and 80<g<200 and b>120
        if pink and start is None:start=x
        if not pink and start is not None:
            if x-start>=3:runs.append((start+x)//2)
            start=None
    for x in runs:
        ps=[im.getpixel((a,b)) for a in range(max(216,x-10),min(775,x+10)) for b in range(282,298)]
        black=sum(max(p)<75 for p in ps);orange=sum(p[0]>170 and 65<p[1]<210 and p[2]<90 for p in ps)
        belt.append('gunkan' if orange>15 and black>60 else ('california' if orange>2 else 'onigiri'))
    red=[x for x in range(640,745) for y in range(88,96) if (lambda p:p[0]>180 and p[1]<150 and p[2]<130)(im.getpixel((x,y)))]
    closing=max(red+[640])>728
    return {'closing':closing,'belt':belt,'orders':orders,'plates':[s for s in plates if s not in {o['seat'] for o in orders}]}
if __name__=='__main__':
    import sys,json
    print(json.dumps(observe(sys.argv[1])))
