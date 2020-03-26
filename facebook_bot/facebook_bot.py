import sys
import time

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class facebook_bot():
    def __init__(self, driver, url, username, password, friends=None):

        # driver: Webdriver path
        # url: Facebook site
        # username: Facebook username
        # password: Facebook password
        # friends: friends: If it's None, the message will port on User's wall.
        # If not, then it will post to the given ids wall.
        # This can be a string, list and dictionary.

        options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--user-data-dir=<Put your Chrome App Data dir>')
        options.add_argument('--profile-directory=Default')

        self.driver = webdriver.Chrome(driver, options=options)
        self.driver.get(url)
        self.friends = friends
        self.login(username, password)

    def show_exception(self, e):
        print(e)
        self.driver.quit()
        sys.exit()

    def login(self, username, password):
        try:
            email_box = self.driver.find_element_by_id('email')
            email_box.send_keys(username)

            pass_box = self.driver.find_element_by_id('pass')
            pass_box.send_keys(password)

            login_btn = self.driver.find_element_by_id('loginbutton')
            login_btn.click()
        except NoSuchElementException as e:
            self.show_exception(e)
        except Exception as e:
            self.show_exception(e)

    def post_on_wall(self, message):

        if self.friends:
            if type(self.friends) == str:
                self.driver.get('http://www.facebook.com/{}'.format(self.friends))
                self.post_message(message)
            if type(self.friends) == dict:
                for key, value in self.friends.items():
                    self.driver.get('http://www.facebook.com/{}'.format(key))
                    self.post_message(message)
            elif type(self.friends) == list:
                for friend in self.friends:
                    self.driver.get('http://www.facebook.com/{}'.format(friend))
                    self.post_message(message)
        else:
            self.post_message(message)

        self.driver.close()

    def post_message(self, message):
        try:
            if self.friends:
                post_box = self.driver.find_element_by_class_name('_1mf')
                btn_xpath = '//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]'
            else:
                post_box = self.driver.find_element_by_tag_name('textarea')
                btn_xpath = '//button[@class="_1mf7 _4r1q _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]'

            post_box.send_keys(message)

            post_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, btn_xpath)))
            post_btn.click()
        except NoSuchElementException as e:
            self.show_exception(e)
        except Exception as e:
            self.show_exception(e)

        time.sleep(5)
