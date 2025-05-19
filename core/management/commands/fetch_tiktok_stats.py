from django.core.management.base import BaseCommand
import asyncio
from core.tiktok_api_utils import fetch_all_tiktok_stats  # ✅ Correct function name

class Command(BaseCommand):
    help = 'Fetch and store TikTok stats for all influencers'

    def handle(self, *args, **kwargs):
        self.stdout.write("📦 Starting TikTok stats import...")
        asyncio.run(fetch_all_tiktok_stats())
        self.stdout.write(self.style.SUCCESS("✅ TikTok stats import completed!"))
