
from django.core.management import call_command
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
import asyncio
from core.tiktok_api_utils import fetch_all_tiktok_stats  # ✅ This must be importable

# ✅ Define a proper top-level function
def run_fetch_task():
    asyncio.run(fetch_all_tiktok_stats())

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # ✅ Use the string path or named function — NOT a lambda
    scheduler.add_job(
        run_fetch_task,                # named function (not lambda!)
        trigger="interval",
        hours=24,
        id="daily_tiktok_stats",
        max_instances=1,
        replace_existing=True,
    )

    print("Scheduler started for TikTok stat collection.")
    scheduler.start()