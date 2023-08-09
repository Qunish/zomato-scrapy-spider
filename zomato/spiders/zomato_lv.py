import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
from selenium.webdriver.common.by import By

USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
]
DRIVER_FILE_PATH = "/Users/qunishdash/Documents/chromedriver_mac64/chromedriver"

class ZomatoSpider(scrapy.Spider):
    name = 'zomato_lv'
    start_urls = ['https://www.zomato.com/bangalore/order-food-online']

    def get_chrome_driver(self, headless_flag):
        # Set up the Selenium webdriver
        chrome_options = Options()

        if headless_flag:
            # in case you want a headless browser
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
        else:
            # in case you want to open the browser
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
            chrome_options.headless = False

        service = Service(executable_path=DRIVER_FILE_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def scroll_to_bottom(self, driver):
        # Allow infinite scrolling by scrolling to the bottom of the page
        screen_height = driver.execute_script("return window.screen.height;")
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        i = 1

        while (screen_height * i) <= scroll_height:
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(3)  # Pause to allow data to load

    def get_card_data(self, card):
        try:
            name = card.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/a[2]/div[1]/h4/text()").text
        except Exception as e:
            name = ''
        result = {
            "name": name,
        }
        return result

    def parse(self, response):
        driver = self.get_chrome_driver(False)
        driver.get(response.url)
        time.sleep(2)  # Allow for the web page to open

        self.scroll_to_bottom(driver)

        # Extract data from the fully loaded page
        all_cards = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div")
        for card in all_cards:
            card_result = self.get_card_data(card)
            yield card_result

        # Close the WebDriver after finishing the scraping process
        driver.quit()

