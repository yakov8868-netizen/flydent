# usage: python3 tools/build_metrics.py rows.json [competitors.json]
# rows.json (LAST 365 DAYS) = Metricool getAnalyticsDataByMetrics output for metrics
#   ["IGEV06","IGEV05","IGEV01","FBEV49","FBEV17"] (last 30 days, brand 7779606)
# competitors.json (optional) = [{"name","handle","followers","posts","reels","avg_likes","engagement","source"}]
import json, sys, datetime
rows = json.load(open(sys.argv[1]))["rows"]
f = lambda v: None if v in (None, "") else round(float(v))
by = {r[5]: {"ig_reach": f(r[0]), "ig_views": f(r[1]), "ig_followers": f(r[2]), "fb_views": f(r[3]), "fb_followers": f(r[4])} for r in rows}
d0 = datetime.datetime.strptime(min(by), "%Y%m%d"); d1 = datetime.datetime.strptime(max(by), "%Y%m%d")
days = []
while d0 <= d1:
    k = d0.strftime("%Y%m%d"); x = by.get(k, {"ig_reach": None, "ig_views": None, "ig_followers": None, "fb_views": None, "fb_followers": None})
    days.append({"d": f"{d0.day}.{d0.month}.{str(d0.year)[2:]}", "iso": d0.strftime("%Y-%m-%d"), **x}); d0 += datetime.timedelta(days=1)
comp = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else (json.load(open("data/competitors.json")) if __import__("os").path.exists("data/competitors.json") else [])
json.dump({"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "days": days, "competitors": comp},
          open("data/metrics.json", "w"), ensure_ascii=False, indent=1)
print(len(days), "days,", len(comp), "competitors")
