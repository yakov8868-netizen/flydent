# Daily site update (manager agent)
1. `python3 tools/build_site_data.py /tmp/agents.json /tmp/activity.json`
2. Metricool getAnalyticsDataByMetrics, brandId 7779606, last 30 days (from = today-30 00:00, to = today 23:59, Asia/Jerusalem),
   metrics exactly in this order: ["IGEV06","IGEV05","IGEV01","FBEV49","FBEV17"]. Save the JSON result ({"rows":[...]}) to /tmp/metrics_rows.json.
3. Competitors: Metricool getAnalyticsDataByMetrics with ["IGCO02","IGCO03","IGCO07","IGCO08","IGCO12","IGCO09","IGCO10"] for the same period.
   If rows come back, write /tmp/competitors.json as a list of {"name": displayName, "handle": screenName, "followers", "posts", "reels", "avg_likes", "engagement"}.
   If empty, skip it (the page shows an explanation). Never invent competitor numbers.
4. `python3 tools/build_metrics.py /tmp/metrics_rows.json [/tmp/competitors.json]`
5. Check data/*.json has no patient names, emails, phone numbers other than 03-6135444, payment/ad-account details or internal URLs.
6. Commit only data/*.json and push.
