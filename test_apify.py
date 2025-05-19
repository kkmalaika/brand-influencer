import os
from dotenv import load_dotenv

load_dotenv()  # 👈 MUST happen before trying to read environment variables

#print("DEBUG: APIFY_TOKEN =", os.getenv("APIFY_TOKEN"))  # 🕵️

from core.utils.apify_client import run_apify_actor

data = run_apify_actor("clockworks~free-tiktok-scraper", {
    "hashtags": ["makeup"],
    "resultsPerPage": 3
})
print(data)


