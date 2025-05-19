import os
import django
from django.utils.timezone import now
from core.models import InfluencerProfile, TikTokStat
from core.utils.apify_client import run_apify_actor

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brand_influencer.settings')
django.setup()

def fetch_and_store_tiktok_stats():
    influencers = InfluencerProfile.objects.filter(platform="TikTok")

    for influencer in influencers:
        if influencer.handle:
            try:
                print(f"Fetching stats for {influencer.handle}...")
                data = run_apify_actor("clockworks~free-tiktok-scraper", {
                    "usernames": [influencer.handle],
                    "resultsPerPage": 1
                })

                if data:
                    item = data[0]
                    followers = item.get("authorMeta", {}).get("fans", 0)
                    likes = item.get("authorMeta", {}).get("heart", 0)
                    videos = item.get("authorMeta", {}).get("video", 0)
                    following = item.get("authorMeta", {}).get("following", 0)

                    TikTokStat.objects.create(
                        influencer=influencer,
                        followers=followers,
                        likes=likes,
                        videos=videos,
                        following=following,
                        date_recorded=now().date()
                    )
                    print(f"✅ Saved stats for {influencer.handle}")
                else:
                    print(f"⚠️ No data found for {influencer.handle}")

            except Exception as e:
                print(f"Error fetching stats for {influencer.handle}: {e}")

if __name__ == "__main__":
    fetch_and_store_tiktok_stats()

