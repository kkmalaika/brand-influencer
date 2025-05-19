from TikTokApi import TikTokApi
import logging
from django.utils.timezone import now
from asgiref.sync import sync_to_async
from .models import InfluencerProfile, TikTokStat

logger = logging.getLogger(__name__)

# --- TikTok cookies from your real browser (✅ Already good)
cookies = [
    {"name": "msToken", "value": "2kJpXih_mIrJlQ9bcgGZHYkRDfWNXwUAW83ihCCY-OnJ6luBA5nmRsIaFzRvkBP_RTohRl1NXliWHq3qSEaaH7pcB2a9INK2M0RNV2Xo7KMED_ztGlz64zoWZ4bl00Q0wMB0VCLLFBDKq67ci9RkL0Ylow==", "domain": ".tiktok.com", "path": "/"},
    {"name": "sessionid", "value": "873edd8459b7eb2856d11bb2b18a67d5", "domain": ".tiktok.com", "path": "/"},
]

# 🧹 REMOVE proxy conflict: we pass NO proxy here now
context_options = {}  # 👈 empty dict = no proxy confusion

# --- One-off fetch for a single influencer
async def get_tiktok_user_stats(username):
    try:
        api = TikTokApi()
        await api.create_sessions(
            num_sessions=1,
            headless=False,         # 👈 Disable headless mode
            browser='webkit',       # 👈 Use webkit (more human-like)
            cookies=cookies,
            context_options=context_options
        )

        user = api.user(username)
        data = await user.info()
        if not data or "userInfo" not in data:
            logger.warning(f"No userInfo returned for @{username}")
            await api.close_sessions()
            return None

        stats = data["userInfo"]["stats"]
        await api.close_sessions()

        # Update influencer profile
        try:
            influencer = await sync_to_async(InfluencerProfile.objects.get)(handle=username)
            influencer.followers = stats["followerCount"]
            await sync_to_async(influencer.save)(update_fields=["followers"])
        except InfluencerProfile.DoesNotExist:
            logger.warning(f"Influencer @{username} not found — skipping DB update.")

        return {
            "username": username,
            "followers": stats["followerCount"],
            "likes": stats["heartCount"],
            "videos": stats["videoCount"],
            "following": stats["followingCount"],
        }

    except Exception as e:
        logger.error(f"Error fetching TikTok data for @{username}: {e}")
        return None

# --- Fetch for all TikTok influencers in DB
async def fetch_all_tiktok_stats():
    try:
        influencers = await sync_to_async(list)(
            InfluencerProfile.objects.filter(platform__iexact="TikTok")
        )

        api = TikTokApi()
        await api.create_sessions(
            num_sessions=1,
            headless=False,  # 👈 Disable headless mode
            browser='webkit',  # 👈 Use webkit (more human-like)
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
