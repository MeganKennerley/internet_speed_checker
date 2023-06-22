from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
TWITTER_EMAIL = "YOUR_EMAIL"
TWITTER_PASSWORD = "YOUR_PASSWORD"


class InternetSpeedTwitterBot():

    def __init__(self, driver_path):
        service = Service(executable_path=driver_path)
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        accept_button = self.driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
        accept_button.click()

        go_button = self.driver.find_element(by=By.CLASS_NAME, value="start-text")
        go_button.click()

        time.sleep(70)
        self.up = self.driver.find_element(by=By.CLASS_NAME, value="upload-speed")
        self.down = self.driver.find_element(by=By.CLASS_NAME, value="download-speed")
        print(self.up.text)
        print(self.down.text)

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/login")

        time.sleep(2)
        email = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]'
                                                            '/form/div/div[1]/label/div/div[2]/div/input')
        password = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/'
                                                               'div[1]/form/div/div[2]/label/div/div[2]/div/input')

        email.send_keys(TWITTER_EMAIL)
        password.send_keys(TWITTER_PASSWORD)
        time.sleep(2)
        password.send_keys(Keys.ENTER)

        time.sleep(5)
        tweet_compose = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/'
                                                                    'div/div/div/div/div[2]/div/div[2]/div[1]/div/div/'
                                                                    'div/div[2]/div[1]/div/div/div/div/div/div/div/div/'
                                                                    'div/div[1]/div/div/div/div[2]/div/div/div/div')

        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for " \
                f"{PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_compose.send_keys(tweet)
        time.sleep(3)

        tweet_button = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/'
                                                                   'div/div/div/div[2]/div/div[2]/div[1]/div/div/div/'
                                                                   'div[2]/div[4]/div/div/div[2]/div[3]')
        tweet_button.click()

        time.sleep(2)
        self.driver.quit()


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()
