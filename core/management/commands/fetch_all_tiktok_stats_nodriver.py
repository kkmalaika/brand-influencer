from django.core.management.base import BaseCommand
import asyncio
import nodriver as uc
from nodriver import cdp
import json
from django.utils.timezone import now
from core.models import InfluencerProfile, TikTokStat
from asgiref.sync import sync_to_async

class Command(BaseCommand):
    help = 'Scrapes TikTok stats by intercepting JSON responses using nodriver CDP handlers'

    def handle(self, *args, **kwargs):
        self.stdout.write("📡 Starting TikTok stats import using nodriver CDP...")
        asyncio.run(self.scrape_via_cdp())
        self.stdout.write(self.style.SUCCESS("✅ All influencer stats successfully scraped and stored!"))

    async def scrape_via_cdp(self):
        try:
            influencers = await sync_to_async(list)(
                InfluencerProfile.objects.filter(platform__iexact="TikTok")
            )

            cookies = [
                {"name": "tt_csrf_token", "value": "7LjwKHbV-kHV3XB794YhnBnaJN9VDdNsrpOw", "domain": ".tiktok.com", "path": "/"},
                {"name": "sessionid", "value": "49e59e1ade252f1e2461477fd6213f46", "domain": ".tiktok.com", "path": "/"}
            ]

            async with await uc.start(headless=False, cookies=cookies) as browser:
                for influencer in influencers:
                    username = influencer.handle.lstrip("@")
                    url = f"https://www.tiktok.com/@{username}"
                    intercepted_data = {}

                    page = await browser.get(url)

                    # Enable network tracking
                    await page.send(cdp.network.enable())

                    # Add a response handler
                    async def on_response(event: cdp.network.ResponseReceived):
                        try:
                            if "user/detail" in event.response.url:
                                response_body = await page.send(cdp.network.get_response_body(event.requestId))
                                if response_body and response_body.body:
                                    json_response = json.loads(response_body.body)
                                    if "userInfo" in json_response:
                                        intercepted_data.update(json_response["userInfo"])
                        except Exception as e:
                            print(f"⚠️ Error parsing response for @{username}: {e}")

                    page.add_handler(cdp.network.ResponseReceived, on_response)

                    # Wait for requests to complete
                    await asyncio.sleep(8)

                    # Extract data
                    followers = 0
                    likes = 0
                    videos = 0
                    try:
                        stats = intercepted_data.get("stats", {})
                        followers = stats.get("followerCount", 0)
                        likes = stats.get("heartCount", 0)
                        videos = stats.get("videoCount", 0)
                        print(f"✅ Intercepted @{username} → followers: {followers}, likes: {likes}, videos: {videos}")
                    except Exception as e:
                        print(f"❌ Could not extract stats for @{username}: {e}")

                    # Store data
                    await sync_to_async(TikTokStat.objects.create)(
                        influencer=influencer,
                        followers=followers,
                        likes=likes,
                        videos=videos,
                        following=0,
                        date_recorded=now()
                    )
                    influencer.followers = followers
                    await sync_to_async(influencer.save)(update_fields=["followers"])

        except Exception as e:
            print(f"❌ Global error: {e}")
