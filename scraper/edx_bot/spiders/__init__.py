from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import EDX_LOGIN, EDX_PASSWORD


class EdXLoggerIn(object):
    '''
    Sign into edX and return the cookies for subsequent requests
    '''
    driver = None
    signin_cookies = set()
    login_href = 'https://courses.edx.org/login'
    dashboard_href = 'https://courses.edx.org/dashboard'

    def __init__(self):
        '''
        When using boot2docker, use the virtual machine's IP address
        (found by running `boot2docker ip`). Otherwise, use localhost
        i.e. 0.0.0.0
        '''
        local_ip = '192.168.59.103'
        self.driver = webdriver.Remote(
           command_executor='http://' + local_ip + ':4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME)

        self.driver.maximize_window()
        self.driver.get(self.login_href)

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
                '//*[@id="my-courses"]')))

        self.driver.get(self.dashboard_href)
        self.signin_cookies = self.driver.get_cookies()


    def close(self):
        self.signin_cookies = set()
        self.driver.close()
