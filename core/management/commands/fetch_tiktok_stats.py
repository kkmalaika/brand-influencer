from django.core.management.base import BaseCommand
from asgiref.sync import async_to_sync
from core.tiktok_api_utils import fetch_and_store_tiktok_stats  # ✅ use the correct async function

class Command(BaseCommand):
    help = "Fetch TikTok stats for a single influencer (testing only)"

    def handle(self, *args, **options):
        username = "princesskotobi"  # 👈 Change to any test handle

        self.stdout.write(f"🔍 Fetching TikTok stats for @{username}...")

        # ✅ Proper async-to-sync call
        result = async_to_sync(fetch_and_store_tiktok_stats)(username)

        if result:
            self.stdout.write(self.style.SUCCESS(f"✅ Stats fetched: {result}"))
        else:
            self.stdout.write(self.style.ERROR(f"❌ Failed to fetch stats for @{username}"))
