import asyncio
import json
from os import path
from playwright.sync_api import sync_playwright
import time

class TwitterScraper:
    def __init__(self, headless=True, username=None, password=None):
        self.headless = headless
        self.username = username
        self.password = password
        self.browser = None

    def login(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=self.headless)
            context = browser.new_context(
                viewport={"width": 1280, "height": 1024},
                default_browser_type="chromium",
            )
            page = context.new_page()
            page.goto("https://twitter.com/i/flow/login")
            page.wait_for_selector("[data-testid='google_sign_in_container']")
            time.sleep(2)
            page.fill('input[type="text"]', self.username)
            time.sleep(2)
            page.locator("//span[text()='Next']").click()
            page.wait_for_selector("[data-testid='LoginForm_Login_Button']")
            time.sleep(2)
            page.fill('input[type="password"]', self.password)
            time.sleep(2)
            page.locator("//span[text()='Log in']").click()
            time.sleep(2)
            context.storage_state(path="state.json")
            time.sleep(2)
            context.close()
            browser.close()

if __name__ == "__main__":
    # Create an instance of the TwitterScraper class with desired parameters
    twitter_bot = TwitterScraper(headless=False, username='YourUsername', password='YourPassword')

    # Call the login method to execute the login process
    twitter_bot.login()
