# usage: python3 tools/build_metrics.py rows.json [competitors.json]
# rows.json = Metricool getAnalyticsDataByMetrics output for metrics
#   ["IGEV06","IGEV05","IGEV01","FBEV49","FBEV17"] (last 30 days, brand 7779606)
# competitors.json (optional) = [{"name","handle","followers","posts","reels","avg_likes","engagement","source"}]
import json, sys, datetime
rows = json.load(open(sys.argv[1]))["rows"]
f = lambda v: None if v in (None, "") else round(float(v))
days = sorted(({"d": r[5], "ig_reach": f(r[0]), "ig_views": f(r[1]), "ig_followers": f(r[2]), "fb_views": f(r[3]), "fb_followers": f(r[4])} for r in rows), key=lambda x: x["d"])
for x in days: x["d"] = f'{x["d"][6:8]}.{int(x["d"][4:6])}'
comp = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else []
json.dump({"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "days": days, "competitors": comp},
          open("data/metrics.json", "w"), ensure_ascii=False, indent=1)
print(len(days), "days,", len(comp), "competitors")
