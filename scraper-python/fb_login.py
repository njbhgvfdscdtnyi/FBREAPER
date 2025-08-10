import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Open Chromium with UI for manual login
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print(" Opening Facebook login page...")
        await page.goto("https://www.facebook.com/login", timeout=60000)

        print(" Please log in manually. Press ENTER here when done.")
        input()  # Wait for user to confirm login

        print(" Saving session to fb_session.json...")
        await context.storage_state(path="fb_session.json")
        print(" Session saved successfully.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
