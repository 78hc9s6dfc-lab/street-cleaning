"""Build data.json from the city's ptillaten.json + servicedagar.json.
Usage: python3 prep.py ptillaten.json servicedagar.json"""
import json, sys, collections as C
pf = sys.argv[1] if len(sys.argv) > 1 else 'ptillaten.json'
sf = sys.argv[2] if len(sys.argv) > 2 else 'servicedagar.json'
P = json.load(open(pf)); S = json.load(open(sf))
WD = {'söndag':0,'måndag':1,'tisdag':2,'onsdag':3,'torsdag':4,'fredag':5,'lördag':6}
DT = {None:0,'vardag utom vardag före sön- och helgdag':1,'vardag före sön- och helgdag':2,'sön- och helgdag':3,'vardag':4}
tabs = {k:[] for k in ['street','dist','zone','type','rate']}
def ix(t, v):
    v = v or ''; L = tabs[t]
    if v not in L: L.append(v)
    return L.index(v)
def enc(coords):
    out=[];px=py=0
    for x,y in coords:
        X=round(x*1e5);Y=round(y*1e5)
        if out and X==px and Y==py: continue
        out+=[X-px,Y-py];px,py=X,Y
    return out
def geom(g): return [enc(l) for l in ([g['coordinates']] if g['type']=='LineString' else g['coordinates'])]
def per(p): return [p['START_MONTH'],p['START_DAY'],p['END_MONTH'],p['END_DAY']] if p.get('START_MONTH') else 0
def ref(p): c=p['CITATION'].split(' ')[1]; return c
def clean_rule(p): return [WD[p['START_WEEKDAY']],p['START_TIME'],p['END_TIME'],per(p),{'jämna veckor':2,'udda veckor':1}.get(p.get('ODD_EVEN'),0)]

sg = C.defaultdict(list)
for f in S['features']:
    p=f['properties']
    if p.get('START_WEEKDAY') in WD: sg[(p['CITATION'],p['EXTENT_NO'])].append(f)
pg = C.defaultdict(list)
for f in P['features']: pg[(f['properties']['CITATION'],f['properties']['EXTENT_NO'])].append(f)

curbs=[]
for k, fs in pg.items():
    ps=[f['properties'] for f in fs]; p0=ps[0]
    usable = any(p['VEHICLE']=='fordon' for p in ps)
    veh = '' if usable else p0['VEHICLE']
    types = sorted({ix('type',p.get('VF_PLATS_TYP')) for p in ps if p.get('VF_PLATS_TYP') not in (None,'7','-')})
    rates = sorted({ix('rate',p.get('PARKING_RATE')) for p in ps})
    mx=[]
    for p in ps:
        mins=(p.get('MAX_HOURS') or 0)*60+(p.get('MAX_MINUTES') or 0)
        if not mins: continue
        if p.get('START_WEEKDAY') or p.get('START_TIME') is None: st,et=0,2400
        else: st,et=p['START_TIME'],p['END_TIME']
        r=[mins,DT.get(p.get('DAY_TYPE'),0),st,et,per(p)]
        if r not in mx: mx.append(r)
    cl=[clean_rule(s['properties']) for s in sg.get(k,[])]
    zone=next((p.get('PARKING_DISTRICT') for p in ps if p.get('PARKING_DISTRICT')),'')
    curbs.append([ix('street',p0.get('STREET_NAME')),ix('dist',p0.get('CITY_DISTRICT')),ix('zone',zone),types,rates,veh,
      p0.get('VF_METER') or 0,p0.get('VF_PLATSER') or 0,ref(p0),max((p.get('VALID_FROM') or '') for p in ps),
      min((p.get('VALID_TO') or '9999') for p in ps).replace('9999',''),cl,mx,geom(fs[0]['geometry'])])
# cleaning / time-ban stretches with no parking regulation
for k, fs in sg.items():
    if k in pg: continue
    p0=fs[0]['properties']
    t=p0.get('VF_PLATS_TYP'); t=None if t in ('7','-') else t
    curbs.append([ix('street',p0.get('STREET_NAME')),ix('dist',p0.get('CITY_DISTRICT')),ix('zone',p0.get('PARKING_DISTRICT')),
      [ix('type',t)] if t else [],[ix('rate',p0.get('PARKING_RATE'))],'',p0.get('VF_METER') or 0,p0.get('VF_PLATSER') or 0,ref(p0),
      p0.get('VALID_FROM') or '',p0.get('VALID_TO') or '',[clean_rule(f['properties']) for f in fs],[],geom(fs[0]['geometry'])])
out={'stamp':P.get('timeStamp'),'t':tabs,'c':curbs}
s=json.dumps(out,ensure_ascii=False,separators=(',',':'))
open('data.json','w').write(s)
print(len(curbs),'curbs',round(len(s)/1e6,2),'MB', sum(1 for c in curbs if c[5]),'reserved', sum(1 for c in curbs if c[12]),'with max time')
