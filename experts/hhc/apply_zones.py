#!/usr/bin/env python3
"""
1700 Pavilion — re-parent ProptechOS sensor twins to the correct tenant zone.
Source of truth: the Niagara BAS tenant tree + Genea Areas (tenant identity).

USAGE
  apply_zones.py snapshot         record current placement of all 287 devices  (READ ONLY)
  apply_zones.py plan             print what would change                      (READ ONLY)
  apply_zones.py apply-one <dev>  patch a single device, verify, report
  apply_zones.py apply            patch everything in the plan
  apply_zones.py rollback         restore every device from the snapshot

Every write records the previous value first. Nothing is patched that is not in
the plan file. Zone creation is NOT done here.
"""
import json,urllib.request,ssl,sys,datetime,collections
S="/private/tmp/claude-501/-Users-erikwallin-eriks-project-proptech-agents/c62d48f1-367d-4a0b-9023-2ab0b41563b3/scratchpad"
API="https://proptechos.com/api/json"
tok=open(S+"/tok").read().strip(); ctx=ssl.create_default_context()

def call(method,path,body=None,ct="application/json"):
    data=json.dumps(body).encode() if body is not None else None
    r=urllib.request.Request(API+path,data=data,method=method,
        headers={"Authorization":"Bearer "+tok,"User-Agent":"curl/8.4.0",
                 "Accept":"application/json","Content-Type":ct})
    try:
        with urllib.request.urlopen(r,timeout=45,context=ctx) as f:
            return f.status,f.read().decode(errors="replace")
    except urllib.error.HTTPError as e: return e.code,e.read()[:300].decode(errors="replace")
    except Exception as e: return None,str(e)[:120]

def preflight():
    c,_=call("GET","/quantitykind")
    if c!=200: print(f"CREDENTIAL FAILURE (HTTP {c}) — token lasts ~60 min."); sys.exit(2)

def get_placement(sid):
    c,b=call("GET",f"/sensor/{sid}")
    return json.loads(b).get("isMountedInBuildingComponent") if c==200 else None

def patch(sid,dest):
    return call("PATCH",f"/sensor/{sid}",
                [{"op":"replace","path":"/isMountedInBuildingComponent","value":dest}],
                ct="application/json-patch+json")

def load_plan():
    return json.load(open(S+"/plan.json"))

cmd=sys.argv[1] if len(sys.argv)>1 else "plan"
preflight()

if cmd=="snapshot":
    PH=json.load(open(S+"/phys.json")); snap={}
    for dev,e in PH.items():
        for k,sid in e.items():
            p=get_placement(sid)
            snap.setdefault(dev,{})[k]={"sensorId":sid,"was":p}
    snap["_ts"]=datetime.datetime.utcnow().isoformat()
    json.dump(snap,open(S+"/snapshot.json","w"),indent=1)
    print(f"snapshot of {len(snap)-1} devices -> snapshot.json")

elif cmd=="plan":
    p=load_plan()
    print(f"{len(p)} sensor moves planned")
    by=collections.Counter(x["to_name"] for x in p)
    for k,n in by.most_common(): print(f"   {n:>4}  -> {k}")

elif cmd in ("apply","apply-one"):
    p=load_plan()
    if cmd=="apply-one":
        want=sys.argv[2]; p=[x for x in p if x["device"]==want]
        if not p: print(f"{want} not in plan"); sys.exit(1)
    done=[];fail=[]
    for x in p:
        before=get_placement(x["sensorId"])
        c,b=patch(x["sensorId"],x["to"])
        after=get_placement(x["sensorId"])
        ok = (c in (200,204)) and after==x["to"]
        (done if ok else fail).append({**x,"before":before,"after":after,"http":c,"body":b[:120]})
        print(f"  {'OK ' if ok else 'FAIL'} {x['device']:<16}{x['sensor']:<10} {str(before)[:8]} -> {str(after)[:8]}  HTTP {c}")
    json.dump({"done":done,"fail":fail,"ts":datetime.datetime.utcnow().isoformat()},
              open(S+"/applied.json","w"),indent=1)
    print(f"\n{len(done)} applied · {len(fail)} failed  -> applied.json")

elif cmd=="rollback":
    snap=json.load(open(S+"/snapshot.json")); n=0
    for dev,e in snap.items():
        if dev=="_ts": continue
        for k,v in e.items():
            if v["was"] is None: continue
            cur=get_placement(v["sensorId"])
            if cur!=v["was"]:
                c,_=patch(v["sensorId"],v["was"]); n+=1
                print(f"  restored {dev} {k} -> {v['was'][:8]}  HTTP {c}")
    print(f"{n} sensors restored")
else:
    print(__doc__)
