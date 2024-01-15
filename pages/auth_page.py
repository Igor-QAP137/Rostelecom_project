from .base import BasePage
from selenium.webdriver.common.by import By

import time,os

class AuthPage(BasePage):

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        url = os.getenv("LOGIN_URL") or "https://b2c.passport.rt.ru"
        driver.get(url)

        self.username = driver.find_element(By.ID, "username")
        self.password = driver.find_element(By.ID, "password")
        self.auth_btn = driver.find_element(By.ID, "kc-login")
        self.forgot = driver.find_element(By.ID, "forgot_password")
        self.register = driver.find_element(By.ID, 'kc-register')
        self.placeholder = driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[2]')
        self.agree = driver.find_element(By.ID, "rt-footer-agreement-link")
        self.vk_btn = driver.find_element(By.ID, "oidc_vk")
        self.ok_btn = driver.find_element(By.ID, 'oidc_ok')
        self.mail_ru_btn = driver.find_element(By.ID, 'oidc_mail')
        self.yandex_btn = driver.find_element(By.ID, 'oidc_ya')


    def btn_click(self):
        self.auth_btn.click()

    def find_element(self, by, location):
        return self.driver.find_element(by, location)

    def get_current_url(self):
        url = urlparse(self.driver.current_url)
        return url.path


class CodePage(BasePage):

    def __init__(self, driver, timeout=5):
        super().__init__(driver, timeout)
        url = os.getenv("LOGIN_URL") or "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk-api.rt.ru%2Fsso-auth%2F%3Fredirect%3Dhttps%253A%252F%252Fstart.rt.ru%252F&response_type=code&scope=openid"
        driver.get(url)

        self.address = driver.find_element(By.ID, "address")
        self.code_btn = driver.find_element(By.ID, "otp_get_code")

    def get_click(self):
        self.code_btn.click()

