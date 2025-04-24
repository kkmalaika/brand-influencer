from TikTokApi import TikTokApi
import logging
from django.utils.timezone import now
from asgiref.sync import sync_to_async
from .models import InfluencerProfile, TikTokStat

logger = logging.getLogger(__name__)

# 🧁 TikTok cookies from your browser
cookies = [
    {"name": "msToken", "value": "your_msToken_here", "domain": ".tiktok.com", "path": "/"},
    {"name": "sessionid", "value": "your_sessionid_here", "domain": ".tiktok.com", "path": "/"},
]

# 🛠️ Playwright proxy config — only here!
context_options = {
    "proxy": {
        "server": "http://51.159.98.163:8089"
    }
}

# --- One-off fetch for a single influencer
async def get_tiktok_user_stats(username):
    try:
        api = TikTokApi()
        await api.create_sessions(
            num_sessions=1,
            headless=False,
            browser='chromium',
            cookies=cookies,
            context_options=context_options
        )

        user = api.user(username)
        data = await user.info()
        await api.close_sessions()

        stats = data["userInfo"]["stats"]
        try:
            influencer = await sync_to_async(InfluencerProfile.objects.get)(handle=username)
            influencer.followers = stats["followerCount"]
            await sync_to_async(influencer.save)(update_fields=["followers"])
        except InfluencerProfile.DoesNotExist:
            logger.warning(f"Influencer @{username} not found — profile not updated.")

        return {
            "username": username,
            "followers": stats["followerCount"],
            "likes": stats["heartCount"],
            "videos": stats["videoCount"],
            "following": stats["followingCount"]
        }

    except Exception as e:
        logger.error(f"Error fetching TikTok data for @{username}: {e}")
        return None

# --- Fetch for all TikTok influencers in the DB
async def fetch_all_tiktok_stats():
    try:
        influencers = await sync_to_async(list)(
            InfluencerProfile.objects.filter(platform__iexact="TikTok")
        )

        api = TikTokApi()
        await api.create_sessions(
            num_sessions=1,
            headless=False,
            browser='chromium',
            cookies=cookies,
            context_options=context_options
        )

        for influencer in influencers:
            try:
                user = api.user(influencer.handle)
                data = await user.info()
                stats = data["userInfo"]["stats"]

                await sync_to_async(TikTokStat.objects.create)(
                    influencer=influencer,
                    followers=stats["followerCount"],
                    likes=stats["heartCount"],
                    videos=stats["videoCount"],
                    following=stats["followingCount"],
                    date_recorded=now()
                )

                influencer.followers = stats["followerCount"]
                await sync_to_async(influencer.save)(update_fields=["followers"])

            except Exception as e:
                logger.error(f"Error processing @{influencer.handle}: {e}")

        await api.close_sessions()
        logger.info("✅ TikTok stats updated for all influencers.")

    except Exception as e:
        logger.error(f"❌ Global fetch error: {e}")

# --- Search top TikTok video for a hashtag
async def fetch_top_influencer_from_hashtag(hashtag):
    try:
        api = TikTokApi()
        await api.create_sessions(
            num_sessions=1,
            headless=False,
            browser='webkit',
            cookies=cookies,
            context_options=context_options
        )

        import asyncio
        await asyncio.sleep(3)

        tag = api.hashtag(name=hashtag)
        videos = [video async for video in tag.videos(count=1)]
        await api.close_sessions()

        if not videos:
            logger.warning(f"No videos found for hashtag #{hashtag}")
            return None

        top_video = videos[0]
        user = top_video.author
        username = user.username

        await get_tiktok_user_stats(username)
        return {"username": username}

    except Exception as e:
        logger.error(f"Error during hashtag search for #{hashtag}: {e}")
        return None
