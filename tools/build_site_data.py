# usage: python3 tools/build_site_data.py agents.json activity.json  -> writes data/*.json (public-safe)
import json, sys, re, datetime
ag = json.load(open(sys.argv[1])); ac = json.load(open(sys.argv[2]))
keep_a = ["id","order","emoji","name","role","cadence","status","last_run","last_result","next_task"]
ag = sorted([{k:a.get(k,"") for k in keep_a} for a in ag], key=lambda a: a["order"])
url = re.compile(r'https?://\S+')
out = []
for e in ac:
    lvl = e.get("level","info"); lvl = lvl if lvl in ("info","attention") else "info"
    out.append({"at": e.get("at",""), "agent": e.get("agent",""), "level": lvl, "action": url.sub("", e.get("action","")).strip()})
out.sort(key=lambda e: e["at"], reverse=True)
json.dump(ag, open("data/agents.json","w"), ensure_ascii=False, indent=1)
json.dump({"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "items": out[:60]}, open("data/activity.json","w"), ensure_ascii=False, indent=1)
print(len(ag), len(out[:60]))
