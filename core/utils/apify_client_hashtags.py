
# core/utils/apify_client_hashtags.py
import requests
import os

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("🚨 APIFY_TOKEN not found. Make sure it's set in .env!")

def run_apify_hashtag_actor(actor_id, input_payload):
    if not APIFY_TOKEN:
        raise ValueError("APIFY_TOKEN not set in environment.")

    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    # ✅ Send the full input_payload, including 'hashtag'
    response = requests.post(url, json=input_payload)

    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Apify Error: {response.status_code} - {response.text}")
