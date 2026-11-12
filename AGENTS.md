# Daily site update (manager agent)
1. `python3 tools/build_site_data.py /tmp/agents.json /tmp/activity.json`
   (keeps level "attention" items — they feed the "דורש תשומת לב" section; the privacy check in step 6 still applies)
2. Metricool getAnalyticsDataByMetrics, brandId 7779606, last 365 days (from = today-365 00:00, to = today 23:59, Asia/Jerusalem),
   metrics exactly in this order: ["IGEV06","IGEV05","IGEV01","FBEV49","FBEV17"]. Save the JSON result ({"rows":[...]}) to /tmp/metrics_rows.json.
3. Same tool, last 60 days, metrics exactly in this order: ["IGEV38","IGEV43","IGEV44","FBEV47","FBEV48"]
   (interactions, IG followers gained/lost, FB followers gained/lost). Save to /tmp/extra_rows.json.
4. Competitors from Metricool (optional): ["IGCO02","IGCO03","IGCO07","IGCO08","IGCO12","IGCO09","IGCO10"] for the last 30 days.
   If rows come back, MERGE them into data/competitors.json (match by handle; update followers/posts/as_of; append new ones). Never delete entries. Never invent numbers.
5. `python3 tools/build_metrics.py /tmp/metrics_rows.json /tmp/extra_rows.json`  (history is kept automatically)
6. Facebook group drafts: copy the dashboard dataset "fb_groups" (read_asset) to data/fb_groups.json when it changed.
7. Privacy check on data/*.json: no patient names, emails, phone numbers other than 03-6135444, card/payment numbers, ad-account ids or internal URLs.
   Attention items may mention a topic ("חשבון המודעות מושהה – לבדוק חיוב") but never account numbers or amounts.
8. Commit only data/*.json and push.

# Competitors (data/competitors.json) — user 12.11.2026: "כל פעם שאתה רואה מתחרה תוסיף"
- Any agent that sees a competitor (Israeli-market dental tourism / Dubai, Turkey, Georgia etc. clinics or agencies targeting Israelis) appends it:
  {"name","market","handle" (Instagram, null if unknown),"followers":null,"posts":null,"as_of":null,"source","added":"YYYY-MM-DD"}.
  Never duplicate (match by name or handle). Never delete entries. Never invent numbers.
- The evening task (user's Chrome) fills handle/followers/posts/as_of from the public Instagram profile.
- build_metrics.py reads data/competitors.json automatically; commit it together with data/*.json.
