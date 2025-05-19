# core/management/commands/fetch_tiktok_stats_apify.py

from django.core.management.base import BaseCommand
from core.models import InfluencerProfile, WatchedInfluencer, TikTokStat
from core.utils.apify_client import run_apify_actor
from django.utils.timezone import now
from datetime import date
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetch and store TikTok stats for all influencers and watched profiles via Apify actor"

    def handle(self, *args, **kwargs):
        self.stdout.write(" Starting Apify TikTok stats import...")

        # Get all TikTok handles from influencer profiles and watched influencers
        influencer_handles = InfluencerProfile.objects.filter(platform__iexact="TikTok").values_list("handle", flat=True)
        watched_handles = WatchedInfluencer.objects.select_related("influencer").values_list("influencer__handle", flat=True)

        all_handles = set(handle.lstrip("@").lower() for handle in influencer_handles) | \
                      set(handle.lstrip("@").lower() for handle in watched_handles)

        if not all_handles:
            self.stdout.write("⚠ No TikTok influencers or watched users to process.")
            return

        input_payload = {
            "profiles": ",".join(sorted(all_handles))  # Apify actor expects comma-separated usernames
        }

        try:
            data = run_apify_actor("kkmalaika~tiktok-agent", input_payload)

            if not data:
                self.stdout.write(self.style.ERROR(" No data returned from Apify."))
                return

            for item in data:
                username = item.get("username", "").strip().lower()
                followers = item.get("followers", 0)
                likes = item.get("likes", 0)
                videos = item.get("videos", 0)
                following = item.get("following", 0)

                if followers == 0 and likes == 0 and videos == 0:
                    self.stdout.write(self.style.WARNING(f"⏭ Skipping @{username}: no meaningful data"))
                    continue

                influencer = InfluencerProfile.objects.filter(handle__iexact=username).first()

                already_exists = TikTokStat.objects.filter(
                    influencer=influencer,
                    date_recorded=date.today()
                ).exists()

                if not already_exists:
                    TikTokStat.objects.create(
                        influencer=influencer,
                        followers=followers,
                        likes=likes,
                        videos=videos,
                        following=following,
                        date_recorded=now()
                    )

                    if influencer:
                        influencer.followers = followers
                        influencer.save(update_fields=["followers"])

                    self.stdout.write(self.style.SUCCESS(f" Stats saved for @{username}: {followers} followers"))
                else:
                    self.stdout.write(f"⏳ Already updated today for @{username}")

            self.stdout.write(self.style.SUCCESS(" All TikTok stats imported via Apify!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f" Error during Apify import: {e}"))
            logger.exception(f"Apify import failed: {e}")
