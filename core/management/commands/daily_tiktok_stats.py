from django.core.management.base import BaseCommand
from django.utils.timezone import localdate, now
from core.models import TikTokStat
import subprocess
import os

class Command(BaseCommand):
    help = "Check if today's TikTok stats exist before triggering the Apify fetch"

    def handle(self, *args, **options):
        today = localdate()

        already_exists = TikTokStat.objects.filter(date_recorded=today).exists()

        timestamp = now().strftime("%Y-%m-%d %H:%M:%S")

        if already_exists:
            self.stdout.write(self.style.WARNING(f"⚠️ [{timestamp}] Today's TikTok stats already exist. Skipping fetch."))
        else:
            self.stdout.write(self.style.SUCCESS(f"🚀 [{timestamp}] No stats found for today. Running Apify fetch..."))
            subprocess.call([
                'python', 'manage.py', 'fetch_tiktok_stats_apify'
            ])
