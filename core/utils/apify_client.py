# core/utils/apify_client.py
import requests
import os

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("🚨 APIFY_TOKEN not found. Make sure it's set in .env!")

def run_apify_actor(actor_id, input_payload):
    if not APIFY_TOKEN:
        raise ValueError("APIFY_TOKEN not set in environment.")

    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    # ⭐ Build final payload correctly
    payload = {
        "profiles": input_payload.get("profiles", [])
    }

    response = requests.post(url, json=payload)

    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Apify Error: {response.status_code} - {response.text}")
