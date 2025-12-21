import json
import boto3
import requests
from datetime import datetime, timedelta

S3_WIKI_BUCKET = "fazile-wikidata"


def lambda_handler(event, context):
    # Determine date to query
    if "date" in event and event["date"]:
        query_date = event["date"]
    else:
        query_date = (datetime.utcnow() - timedelta(days=21)).strftime("%Y-%m-%d")

    year, month, day = query_date.split("-")

    # Wikimedia Pageviews API
    url = (
        "https://wikimedia.org/api/rest_v1/"
        f"metrics/pageviews/top/en.wikipedia/all-access/{year}/{month}/{day}"
    )

    headers = {
        "User-Agent": "CEU-DataEngineering-Homework/1.0 (contact: student@ceu.edu)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    articles = data["items"][0]["articles"]

    retrieved_at = datetime.utcnow().isoformat()
    records = []

    for article in articles:
        records.append({
            "title": article["article"],
            "views": article["views"],
            "rank": article["rank"],
            "date": query_date,
            "retrieved_at": retrieved_at
        })

    body = "\n".join(json.dumps(r) for r in records)

    s3 = boto3.client("s3")
    s3_key = f"raw-views/raw-views-{query_date}.json"

    s3.put_object(
        Bucket=S3_WIKI_BUCKET,
        Key=s3_key,
        Body=body
    )

    return {
        "statusCode": 200,
        "body": f"Uploaded page views data to raw-views/{s3_key}"
    }
