from django.core.management.base import BaseCommand
from core.models import InfluencerProfile, TikTokStat
from core.tiktok_api_utils import get_tiktok_user_stats
import asyncio
from datetime import datetime


class Command(BaseCommand):
    help = "Fetch TikTok stats for all influencers and store them"

    def handle(self, *args, **kwargs):
        # Get all influencers with TikTok handles
        influencers = InfluencerProfile.objects.exclude(handle="").exclude(platform__iexact="")

        loop = asyncio.get_event_loop()

        for influencer in influencers:
            username = influencer.handle.strip()
            print(f"Fetching stats for @{username}...")

            try:
                data = loop.run_until_complete(get_tiktok_user_stats(username))
                if data:
                    TikTokStat.objects.create(
                        influencer=influencer,
                        followers=data["followers"],
                        likes=data["likes"],
                        videos=data["videos"],
                        following=data["following"],
                        date_recorded=datetime.now()
                    )
                    print(f"✅ Stats saved for @{username}")
                else:
                    print(f"⚠️ No data returned for @{username}")

            except Exception as e:
                print(f"❌ Failed for @{username}: {e}")
