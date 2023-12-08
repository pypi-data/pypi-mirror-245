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
    
    @staticmethod
    def search_user(user_input: str) -> dict:
        _xhr_calls = []

        def intercept_response(response):
            if response.request.resource_type == "xhr":
                _xhr_calls.append(response)
            return response

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1920, "height": 1080}, storage_state="state.json")
            page = context.new_page()

            page.on("response", intercept_response)
            page.goto(f"https://twitter.com/search?q={user_input}&src=typed_query&f=user")
            page.wait_for_selector("[data-testid='cellInnerDiv']")
            time.sleep(5)

            for f in _xhr_calls:
                if re.search("SearchTimeline", f.url):
                    tweet_calls = [f]
                    break

            users = []
            for xhr in tweet_calls:
                data = xhr.json()
                search_result = data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][1]['entries']
            
            del search_result[-2:]

            for sr in search_result:
                try:
                    legacy = sr['content']['itemContent']['user_results']['result']
                    users.append({
                        "user_id" : legacy['rest_id'],
                        "name" : legacy['legacy']['name'],
                        "screen_name" : legacy['legacy']['screen_name'],
                        "bio" : legacy['legacy']['description'],
                        "location" : legacy['legacy']['location'],
                        "followers" : legacy['legacy']['followers_count'],
                        "following" : legacy['legacy']['friends_count'],
                        "tweets" : legacy['legacy']['statuses_count'],
                        "favorites" : legacy['legacy']['favourites_count'],
                        "private" : legacy['legacy']['protected']  if 'protected' in legacy['legacy'] else False,
                        "verified" : legacy['is_blue_verified'],
                        "avatar" : legacy['legacy']['profile_image_url_https'],
                        "created" : legacy['legacy']['created_at'],
                    })
                except:
                    pass

            return users

if __name__ == "__main__":
    # Create an instance of the TwitterScraper class with desired parameters
    twitter_bot = TwitterScraper(headless=False, username='YourUsername', password='YourPassword')

    # Call the login method to execute the login process
    twitter_bot.login()
