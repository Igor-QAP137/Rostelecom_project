from pages.auth_page import AuthPage
from pages.auth_page import CodePage
import time
import pickle
import selenium
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from time import sleep
from settings import valid_email, valid_password, valid_number, valid_login, valid_account

#python -m pytest -sv --driver Chrome --driver-path chromedriver.exe tests/test_rostelecom.py

# TC-RT-001 (открываем страницу авторизации)
def test_the_main_page_is_open(selenium):
    page = AuthPage(selenium)
    time.sleep(3) # задержка для учебных целей
    assert page.get_base_url() == 'b2c.passport.rt.ru'

# TC-RT-005 (проверяем что по умолчанию страница авторизации открывается на вкладке "Телефон")
def test_phone_by_default(selenium):
    page = AuthPage(selenium)
    time.sleep(3) # задержка для учебных целей
    assert page.placeholder.text == 'Мобильный телефон'

# TC-RT-006 (проверяем что вкладки на странице авторизации переключаются автоматически при указании
# телефона/почты/логина/лицевого счета)
def test_automatic_tab_selection(selenium):
    page = AuthPage(selenium)

    # вводим номер телефона
    page.username.send_keys('+70000000000')
    page.password.send_keys('hgfjgfjhmghg')
    sleep(5)

    assert page.placeholder.text == 'Мобильный телефон'

    # очищаем поле логин
    page.username.send_keys(Keys.CONTROL, 'a')
    page.username.send_keys(Keys.DELETE)

    # вводим почту
    page.username.send_keys('validemail@gmail.com')
    page.password.send_keys('jhjhvjfjgfjhghg')
    sleep(5)

    assert page.placeholder.text == 'Электронная почта'

    # очищаем поле логин
    page.username.send_keys(Keys.CONTROL, 'a')
    page.username.send_keys(Keys.DELETE)

    # вводим логин
    page.username.send_keys('Test')
    page.password.send_keys('chxjchdd')
    sleep(5)

    assert page.placeholder.text == 'Логин'

    # очищаем поле логин
    page.username.send_keys(Keys.CONTROL, 'a')
    page.username.send_keys(Keys.DELETE)

    # вводим номер лицевого счета
    page.username.send_keys('012345678910')
    page.password.send_keys('hbdsjvbdjfbv')
    sleep(5)

    assert page.placeholder.text == 'Лицевой счёт'

# TC-RT-007 (Вход в личный кабинет с валидными данными "номер телефона" и "пароль")
def test_auth_reg_phone_pass(selenium):
    page = AuthPage(selenium)

    # вводим номер телефона и пароль
    page.username.send_keys(valid_number)
    page.password.send_keys(valid_password)
    sleep(15) # на случай появления Captcha, вводим вручную
    page.btn_click()

    #assert page.get_current_url() == '/account_b2c/page'
    assert page.find_element(By.TAG_NAME, 'h3').text == "Учетные данные"

# TC-RT-008 НЕГАТИВНЫЙ(авторизация по незарегистрированным телефону и паролю)
def test_auth_reg_fake_phone_pass(selenium):
    page = AuthPage(selenium)

    # вводим телефон и пароль
    page.username.send_keys('+70000000000')
    page.password.send_keys('fakepass')
    sleep(15) # на случай появления Captcha, вводим вручную
    page.btn_click()

    err_mess = page.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'

# TC-RT-009 (Вход в личный кабинет с валидными данными "почта" и "пароль")
def test_auth_reg_email_pass(selenium):
    page = AuthPage(selenium)

    # вводим почту и пароль
    page.username.send_keys(valid_email)
    page.password.send_keys(valid_password)
    sleep(15) # на случай появления Captcha, вводим вручную
    page.btn_click()

    assert page.get_relative_link() == '/account_b2c/page'

# TC-RT-010 НЕГАТИВНЫЙ (Вход в личный кабинет с невалидными данными "почта" и "пароль")
def test_auth_reg_fake_email_pass(selenium):
    page = AuthPage(selenium)

    # вводим почту и пароль
    page.username.send_keys('fakeemail@@@mail.ru')
    page.password.send_keys('facepass')
    sleep(15) # на случай появления Captcha, вводим вручную
    page.btn_click()

    err_mess = page.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'

# TC-RT-011 (Вход в личный кабинет с валидными данными "логин" и "пароль")
def test_auth_reg_login_pass(selenium):
    page = AuthPage(selenium)
    page.find_element(By.ID, 't-btn-tab-login').click()
    # вводим логин и пароль
    page.username.send_keys(valid_login)
    page.password.send_keys(valid_password)
    sleep(15) # на случай появления Captcha, вводим вручную
    page.btn_click()

    assert page.get_relative_link() == '/account_b2c/page'

# TC-RT-012 НЕГАТИВНЫЙ(Вход в личный кабинет с невалидными данными "логин" и "пароль")
def test_auth_reg_fake_login_pass(selenium):
    page = AuthPage(selenium)
    page.find_element(By.ID, 't-btn-tab-login').click()
    # вводим логин и пароль
    page.username.send_keys('fakelogin')
    page.password.send_keys('fakepass')
    sleep(15) # на случай появления Captcha, вводим вручную
    page.btn_click()

    err_mess = page.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'

# TC-RT-013 (Вход в личный кабинет с валидными данными "лицевой счет" и "пароль")
def test_auth_reg_account_pass(selenium):
    page = AuthPage(selenium)
    page.find_element(By.ID, 't-btn-tab-ls').click()
    # вводим номер лицевого счёта и пароль
    page.username.send_keys(valid_account)
    page.password.send_keys(valid_password)
    sleep(25) # на случай появления Captcha, вводим вручную
    page.btn_click()

    assert page.get_relative_link() == '/account_b2c/page'

# TC-RT-014 (авторизация по незарегистриванному лицевому счёту и незарегистрированному паролю)
def test_auth_reg_fake_account_pass(selenium):
    page = AuthPage(selenium)
    page.find_element(By.ID, 't-btn-tab-ls').click()
    # вводим номер лицевого счёта и пароль
    page.username.send_keys('777777777777')
    page.password.send_keys('fakepass')
    sleep(15) # на случай появления Captcha, вводим вручную
    page.btn_click()

    err_mess = page.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'

# TC-RT-015 (Форма авторизации по временному коду загружается на странице, создаем скриншот страницы)
def test_page_code_form(selenium):
    page = CodePage(selenium)
    page.driver.save_screenshot('screen_TC-RT-015.jpg')

# TC-RT-016 (авторизация по одноразовому коду через валидный номер телефона)
def test_auth_code_telefon(selenium):
    page = CodePage(selenium)

    # ввод номера телефона
    page.address.send_keys(valid_number)

    sleep(15) # на случай появления Captcha, вводим вручную
    page.get_click()

    otc = page.driver.find_element(By.ID, 'rt-code-0')
    assert otc

#TC-TR-018 (Ввод временного когда в форме авторизации для входа полученного на валидную почту)
def test_auth_code_email(selenium):
    page = CodePage(selenium)

    # ввод номера телефона
    page.address.send_keys(valid_email)

    sleep(25) # на случай появления Captcha, вводим вручную
    page.get_click()

    otc = page.driver.find_element(By.ID, 'rt-code-0')
    assert otc

# TC-RT-019 (Негативный тест на вход в ЛК по временному кода с невалидным номером телефона)
def test_auth_code_no_valid_telefon(selenium):
    page = CodePage(selenium)

    # ввод номера телефона
    page.address.send_keys('800000000')

    sleep(25) # на случай появления Captcha, вводим вручную
    page.get_click()

    reset_pass = page.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div[1]/div/form/div[1]/div/span')
    assert reset_pass.text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'

# TC-RT-020 (Негативный тест на вход в ЛК по временному коду с невалидным адресом email)
def test_auth_code_no_valid_email(selenium):
    page = CodePage(selenium)

    # ввод номера телефона
    page.address.send_keys('fakeemail@@@MaIl.co')

    sleep(25) # на случай появления Captcha, вводим вручную
    page.get_click()

    reset_pass = page.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div[1]/div/form/div[1]/div/span')
    assert reset_pass.text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'

# TC-RT-021 (Кнопка "Забыл пароль" открывает форму восстановление пароля.)
def test_recovery(selenium):
    page = AuthPage(selenium)

    # нажимаем на кнопку "Забыл пароль"
    page.forgot.click()
    sleep(5)

    reset_pass = page.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'

# TC-RT-022 (Форма "регистрация" доступна для заолнения данных)
def test_reg_form(selenium):
    page = AuthPage(selenium)

    # нажимаем на кнопку "Зарегистрироваться"
    page.register.click()
    sleep(5)

    reset_pass = page.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'

# TC-RT-023 (Кнопка "Пользоватльское соглашение" открывает страницу с информацией.)
def test_user_agreement(selenium):
    page = AuthPage(selenium)

    original_window = page.driver.current_window_handle
    # нажимаем на кнопку "Пользовательским соглашением" в футере страницы
    page.agree.click()
    sleep(5)
    WebDriverWait(page.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in page.driver.window_handles:
        if window_handle != original_window:
            page.driver.switch_to.window(window_handle)
            break
    title_page = page.driver.execute_script("return window.document.title")

    assert title_page == 'Пользовательское соглашение'

# TC-RT-024 (Кнопка "vk.com" открывает форму для авторизации через соц сеть.)
def test_auth_vk(selenium):
    page = AuthPage(selenium)
    page.vk_btn.click()
    sleep(5)

    assert page.get_base_url() == 'id.vk.com'

# TC-RT-025 (Кнопка "ok.ru" открывает форму для авторизации через соц сеть.)
def test_auth_ok(selenium):
    page = AuthPage(selenium)
    page.ok_btn.click()
    sleep(5)

    assert page.get_base_url() == 'connect.ok.ru'

# TC-RT-026 (Кнопка "mail.ru  открывает форму для авторизации через соц сеть.)
def test_auth_mail_ru(selenium):
    page = AuthPage(selenium)
    page.mail_ru_btn.click()
    sleep(5)

    assert page.get_base_url() == 'connect.mail.ru'

# TC-RT-027 (Кнопка "yandex.ru" открывает форму авторизации через яндекс аккаунт)
def test_auth_yandex(selenium):
    page = AuthPage(selenium)
    page.yandex_btn.click()
    sleep(5)

    assert page.get_base_url() == 'passport.yandex.ru'




