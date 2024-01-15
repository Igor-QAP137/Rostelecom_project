#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time
from termcolor import colored

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

class BasePage(object):
    # конструктор класса - спец. метод с ключевым словом __init__
    # нам нужны объекты вэб-драйвера адрес страницы и время ожидания эл-тов

    def __init__(self, driver, url, timeout=10):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)

    def get_relative_link(self):
        url = urlparse(self.driver.current_url)
        return url.path

    def get_current_url(self):
        url = urlparse(self.driver.current_url)
        return url.path

    def get_base_url(self):
        url = urlparse(self.driver.current_url)
        return url.hostname

def wait_for_animation(web_browser, selector):

    WebDriverWait(web_browser, 10).until(lambda web_browser:  browser.execute_script(
            'return jQuery(%s).is(":animated")' % json.dumps(selector))
            == False)









