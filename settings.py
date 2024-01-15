import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv(valid_email)
valid_password = os.getenv(valid_password)
valid_number = os.getenv(valid_number)
valid_login = os.getenv(valid_login)
valid_account = os.getenv(valid_account)

url_base_page = "https://b2c.passport.rt.ru/"