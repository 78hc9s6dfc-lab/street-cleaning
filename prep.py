import json,re
import sys
src=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'servicedagar.json'))
WD={'måndag':1,'tisdag':2,'onsdag':3,'torsdag':4,'fredag':5,'lördag':6,'söndag':0}
tabs={'rate':[],'type':[],'dist':[],'street':[]}
def ix(t,v):
    v=v or ''
    L=tabs[t]
    if v not in L: L.append(v)
    return L.index(v)
def enc(coords):
    out=[];px=py=0
    for x,y in coords:
        X=round(x*1e5);Y=round(y*1e5)
        if out and X==px and Y==py: continue
        out+= [X-px,Y-py];px,py=X,Y
    return out
rows=[]
for ft in src['features']:
    p=ft['properties'];g=ft['geometry']
    lines=[g['coordinates']] if g['type']=='LineString' else g['coordinates']
    m=re.search(r'BeslutadAr=(\d+)&LopNr=(\d+)',p['RDT_URL'])
    per=[p['START_MONTH'],p['START_DAY'],p['END_MONTH'],p['END_DAY']] if p.get('START_MONTH') else 0
    oe={'jämna veckor':2,'udda veckor':1}.get(p.get('ODD_EVEN'),0)
    rows.append([ix('street',p.get('STREET_NAME')),ix('dist',p.get('CITY_DISTRICT') or p.get('PARKING_DISTRICT')),
      ix('type',p.get('VF_PLATS_TYP')),ix('rate',p.get('PARKING_RATE')),WD[p['START_WEEKDAY']],p['START_TIME'],p['END_TIME'],
      per,oe,p.get('VALID_FROM') or '',p.get('VALID_TO') or '',p.get('VF_METER') or 0,p.get('VF_PLATSER') or 0,
      m.group(1)+'-'+m.group(2),[enc(l) for l in lines]])
out={'stamp':src.get('timeStamp'),'t':tabs,'f':rows}
s=json.dumps(out,ensure_ascii=False,separators=(',',':'))
open('data.json','w').write(s);print(len(s)/1e6,'MB',src.get('timeStamp'))
