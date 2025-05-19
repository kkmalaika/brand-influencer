import asyncio
import nodriver as uc

async def main():
    # Start Chromium browser (can change to firefox or webkit if installed)
    async with await uc.start(headless=False) as browser:
        page = await browser.get("https://www.tiktok.com/tag/mascara")
        await asyncio.sleep(5)  # give it time to load

        # Find all anchor tags pointing to user profiles
        anchors = await page.query_selector_all("a[href^='/@']")
        usernames = set()

        for anchor in anchors:
            href = anchor.get("href")  # ✅ this is the fix
            if href and href.startswith("/@"):
                usernames.add(href)

        print("👤 Extracted Usernames:")
        for username in list(usernames)[:5]:
            print("-", username)

if __name__ == "__main__":
    asyncio.run(main())
