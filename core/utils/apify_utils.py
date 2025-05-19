# core/tiktok_api_utils.py

from core.models import InfluencerProfile, TikTokStat
from core.utils.apify_client import run_apify_actor
from django.utils.timezone import now
from datetime import date

def fetch_apify_stats_for_handles(handles: list[str]) -> dict:
    """
    Fetch TikTok stats for a list of usernames using Apify.
    Returns a dictionary: {username: {"followers": ..., "likes": ..., "videos": ..., ...}}
    """
    clean_handles = [h.strip().lstrip("@").lower() for h in handles if h.strip()]
    input_payload = {"profiles": ",".join(clean_handles)}

    try:
        data = run_apify_actor("kkmalaika~tiktok-agent", input_payload)
        result = {}

        for item in data:
            username = item.get("username", "").strip().lower()
            followers = item.get("followers", 0)
            likes = item.get("likes", 0)
            videos = item.get("videos", 0)
            following = item.get("following", 0)

            if not username or (followers == 0 and likes == 0 and videos == 0):
                continue

            # Optional: update InfluencerProfile and TikTokStat if user exists
            influencer = InfluencerProfile.objects.filter(handle__iexact=username).first()
            if influencer:
                influencer.followers = followers
                influencer.save(update_fields=["followers"])

                if not TikTokStat.objects.filter(influencer=influencer, date_recorded=date.today()).exists():
                    TikTokStat.objects.create(
                        influencer=influencer,
                        followers=followers,
                        likes=likes,
                        videos=videos,
                        following=following,
                        date_recorded=now()
                    )

            result[username] = {
                "followers": followers,
                "likes": likes,
                "videos": videos,
                "following": following,
            }

        return result

    except Exception as e:
        print(f"[Apify] ❌ Error while fetching TikTok stats: {e}")
        return {}
