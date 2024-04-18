from time import sleep
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

DELAY = 10
ROOM_CODE = 'laz-gpzf-zmi'


class ScrapeThread(threading.Thread):
    def __init__(self, email, password, time_for_sleep: int = 120):
        threading.Thread.__init__(self)
        self.url = f'https://avalon-card-game-egor.vercel.app/'
        self.email = email
        self.password = password
        self.time_for_sleep = time_for_sleep

    def run(self):
        browser = webdriver.Firefox()

        browser.get('https://avalon-card-game-egor.vercel.app/')

        # login page
        try:
            email_input = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]')))
            email_input.send_keys(self.email)
        except TimeoutException:
            print('TimeoutException email')

        try:
            password_input = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
            password_input.send_keys(self.password)
        except TimeoutException:
            print('TimeoutException password')

        try:
            button_login = WebDriverWait(browser, DELAY).until(EC.element_to_be_clickable((By.XPATH, '//button')))
            button_login.click()
        except TimeoutException:
            print('TimeoutException click login')

        # room login page
        WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, '//h2[text()="Last Sessions"]')))
        try:
            room_code_input = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, '//input')))
            room_code_input.send_keys(ROOM_CODE)
        except TimeoutException:
            print('TimeoutException room code')

        try:
            button_login = WebDriverWait(browser, DELAY).until(EC.element_to_be_clickable((By.XPATH, '//button')))
            button_login.click()
        except TimeoutException:
            print('TimeoutException click room')

        sleep(self.time_for_sleep)
        browser.close()