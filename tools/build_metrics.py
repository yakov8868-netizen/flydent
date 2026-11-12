# usage: python3 tools/build_metrics.py /tmp/metrics_rows.json [/tmp/extra_rows.json] [competitors.json]
# metrics_rows.json = Metricool getAnalyticsDataByMetrics, brand 7779606, LAST 365 DAYS,
#   metrics in this order: ["IGEV06","IGEV05","IGEV01","FBEV49","FBEV17"]  (date is the last column)
# extra_rows.json (optional, file name must end with extra_rows.json) = same call, last 60 days,
#   metrics in this order: ["IGEV38","IGEV43","IGEV44","FBEV47","FBEV48"]
# competitors.json (optional) – default: data/competitors.json
# History is kept: existing data/metrics.json days are merged, then trimmed to the last 366 days.
import json, sys, os, datetime

f = lambda v: None if v in (None, "") else round(float(v))
BASE = ("ig_reach", "ig_views", "ig_followers", "fb_views", "fb_followers")
EXTRA = ("ig_interactions", "ig_gained", "ig_lost", "fb_gained", "fb_lost")
ALL = BASE + EXTRA

by = {}
if os.path.exists("data/metrics.json"):
    for x in json.load(open("data/metrics.json")).get("days", []):
        if x.get("iso"):
            by[x["iso"].replace("-", "")] = {k: x.get(k) for k in ALL}

def merge(path, keys):
    for r in json.load(open(path))["rows"]:
        day = r[-1]
        row = by.setdefault(day, {k: None for k in ALL})
        for i, k in enumerate(keys):
            v = f(r[i])
            if v is not None or row.get(k) is None:
                row[k] = v

merge(sys.argv[1], BASE)
rest = sys.argv[2:]
for a in [a for a in rest if a.endswith("extra_rows.json")]:
    merge(a, EXTRA)
args = [a for a in rest if not a.endswith("extra_rows.json")]

cut = (datetime.datetime.now() - datetime.timedelta(days=366)).strftime("%Y%m%d")
by = {k: v for k, v in by.items() if k >= cut}

d0 = datetime.datetime.strptime(min(by), "%Y%m%d")
d1 = datetime.datetime.strptime(max(by), "%Y%m%d")
days = []
while d0 <= d1:
    key = d0.strftime("%Y%m%d")
    vals = by.get(key, {})
    days.append({"d": f"{d0.day}.{d0.month}.{str(d0.year)[2:]}", "iso": d0.strftime("%Y-%m-%d"),
                 **{k: vals.get(k) for k in ALL}})
    d0 += datetime.timedelta(days=1)

if args:
    comp = json.load(open(args[0]))
elif os.path.exists("data/competitors.json"):
    comp = json.load(open("data/competitors.json"))
else:
    comp = []

json.dump({"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "days": days, "competitors": comp},
          open("data/metrics.json", "w"), ensure_ascii=False, indent=1)
print(len(days), "days,", len(comp), "competitors")
