from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from edx_bot.spiders.config import EDX_LOGIN, EDX_PASSWORD


class EdXLoggerIn(object):
    '''
    Sign into edX and return the cookies for subsequent requests
    '''
    
    signin_cookies = set()
    login_page = 'https://courses.edx.org/login'


    def get_signin_cookies(self):
        if self.sign_in_cookies:
            return self.sign_in_cookies

        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(self.login_page)

        form = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]')))
        email = WebDriverWait(form, 10).until(
            EC.visibility_of_element_located((By.ID, 'login-email')))

        email.send_keys(EDX_LOGIN)

        password = form.find_element_by_xpath('//*[@id="login-password"]')
        password.send_keys(EDX_PASSWORD)

        login = form.find_element_by_xpath('//*[@id="login"]/button')
        login.click()

        # Random element within the page... when it loads, we'll be "in"
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                '//*[@id="dashboard-main"]/section[1]/header/h2/span[2]')))

        self.driver.get('https://courses.edx.org/dashboard')
        self.signin_cookies = self.driver.get_cookies()

        self.driver.close()
        return self.signin_cookies


    def delete_signin_cookies(self):
        self.signin_cookies = set()
