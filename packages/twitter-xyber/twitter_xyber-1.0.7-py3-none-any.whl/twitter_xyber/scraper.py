import asyncio
import json
from os import path
from playwright.sync_api import sync_playwright
import time
import re
import json

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
    
    def search_user(self, user_input: str) -> dict:
        _xhr_calls = []

        def intercept_response(response):
            if response.request.resource_type == "xhr":
                _xhr_calls.append(response)
            return response

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=self.headless)
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

    def following_user(self, username: str) -> dict:
        _xhr_calls = []

        def intercept_response(response):
            if response.request.resource_type == "xhr":
                _xhr_calls.append(response)
            return response

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=self.headless)
            context = browser.new_context(viewport={"width": 1920, "height": 1080}, storage_state="state.json")
            page = context.new_page()

            page.on("response", intercept_response)
            page.goto(f"https://twitter.com/{username}/following")
            page.wait_for_selector("[data-testid='cellInnerDiv']")
            time.sleep(5)

            for f in _xhr_calls:
                if re.search("Following", f.url):
                    following_calls = [f]
                    break

            users = []
            for xhr in following_calls:
                data = xhr.json()
                instruction = data['data']['user']['result']['timeline']['timeline']['instructions']
                following_result = next(ins['entries'] for ins in instruction if ins['type'] == 'TimelineAddEntries')

            del following_result[-2:]

            for fr in following_result:
                try:
                    legacy = fr['content']['itemContent']['user_results']['result']
                    users.append({
                        "id" : legacy['rest_id'],
                        "name" : legacy['legacy']['name'],
                        "username" : legacy['legacy']['screen_name'],
                        "followers" : legacy['legacy']['followers_count'],
                        "following" : legacy['legacy']['friends_count'],
                        "url" : '',
                        "tweets" : legacy['legacy']['statuses_count'],
                        "profile_image_url_https" : legacy['legacy']['profile_image_url_https'],
                        "created" : legacy['legacy']['created_at'],
                    })
                except:
                    pass

            return users

    def followers_user(self, username: str) -> dict:
        _xhr_calls = []

        def intercept_response(response):
            if response.request.resource_type == "xhr":
                _xhr_calls.append(response)
            return response

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=self.headless)
            context = browser.new_context(viewport={"width": 1920, "height": 1080}, storage_state="state.json")
            page = context.new_page()

            page.on("response", intercept_response)
            page.goto(f"https://twitter.com/{username}/followers")
            page.wait_for_selector("[data-testid='cellInnerDiv']")
            time.sleep(5)

            for f in _xhr_calls:
                if re.search("Followers", f.url):
                    followers_calls = [f]
                    break

            users = []
            for xhr in followers_calls:
                data = xhr.json()
                instruction = data['data']['user']['result']['timeline']['timeline']['instructions']
                followers_result = next(ins['entries'] for ins in instruction if ins['type'] == 'TimelineAddEntries')

            del followers_result[-2:]

            for fr in followers_result:
                try:
                    legacy = fr['content']['itemContent']['user_results']['result']
                    users.append({
                        "id" : legacy['rest_id'],
                        "name" : legacy['legacy']['name'],
                        "username" : legacy['legacy']['screen_name'],
                        "followers" : legacy['legacy']['followers_count'],
                        "following" : legacy['legacy']['friends_count'],
                        "url" : '',
                        "tweets" : legacy['legacy']['statuses_count'],
                        "profile_image_url_https" : legacy['legacy']['profile_image_url_https'],
                        "created" : legacy['legacy']['created_at'],
                    })
                except:
                    pass

            return users

    def timeline_tweet(self, username: str) -> dict:
        _xhr_calls = []
        tweet_count = 80
        min_count = 20
        max_count = 100

        def intercept_response(response):
            """capture all background requests and save them"""
            # we can extract details from background requests
            if response.request.resource_type == "xhr":
                _xhr_calls.append(response)
            return response

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=self.headless)
            context = browser.new_context(viewport={"width": 1800, "height": 1080}, storage_state="state.json")
            page = context.new_page()

            # enable background request intercepting:
            page.on("response", intercept_response)
            # go to url and wait for the page to load
            page.goto(f"https://twitter.com/{username}")
            page.wait_for_selector("[data-testid='cellInnerDiv']")
            time.sleep(5)
            
            _prev_height = -1
            _max_scrolls = int(round(tweet_count / 20, 0)) if tweet_count >= min_count and tweet_count <= max_count else 1
            _scroll_count = 0

            tweets = []
            print('max scroll :', _max_scrolls)
            while _scroll_count < _max_scrolls:
                # print('start scroll ke ', _scroll_count)
                # Execute JavaScript to scroll to the bottom of the page
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                # Wait for new content to load (change this value as needed)
                page.wait_for_timeout(1000)
                # Check whether the scroll height changed - means more pages are there
                new_height = page.evaluate("document.body.scrollHeight")
                if new_height == _prev_height:
                    break
                _prev_height = new_height
                _scroll_count += 1
                # print('scroll end')
                time.sleep(10)

                # print('start scanning xhr.....')
                # find all tweets background requests:
                for f in _xhr_calls:
                    if re.search("UserTweets", f.url):
                        user_tweets_calls = [f]
                        break

                # print('start collecting data tweets....')
                for xhr in user_tweets_calls:
                    data = xhr.json()
                    instruction = data['data']['user']['result']['timeline_v2']['timeline']['instructions']
                    tweet_result = next(ins['entries'] for ins in instruction if ins['type'] == 'TimelineAddEntries')

                del tweet_result[-2:]

                for tr in tweet_result:
                    try:
                        tweets.append(tr['content'])
                    except:
                        pass
                # print('finish collecting data tweets....')

                # print('finish scanning ')
            # with open('timeline.json', 'w') as f:
            #     json.dump(tweets, f)
            context.close()
            browser.close()
            return tweets

if __name__ == "__main__":
    # Create an instance of the TwitterScraper class with desired parameters
    twitter_bot = TwitterScraper(headless=False, username='YourUsername', password='YourPassword')

    # Call the login method to execute the login process
    twitter_bot.login()
