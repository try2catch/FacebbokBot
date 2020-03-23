import sys

from selenium import webdriver
from selenium.common.exceptions import *


class facebook_bot():
    def __init__(self, driver, url, username, password):
        options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--user-data-dir=<Put your Chrome App Data dir>')
        options.add_argument('--profile-directory=Default')

        self.driver = webdriver.Chrome(driver, options=options)
        self.driver.get(url)
        # self.login(username, password)

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
        post_box = self.driver.find_element_by_tag_name('textarea')
        post_box.send_keys(message)

        while True:
            try:
                post_btn = self.driver.find_element_by_xpath(
                    '//button[@class="_1mf7 _4r1q _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]')
                post_btn.click()
                break
            except NoSuchElementException:
                pass
            except Exception as e:
                self.show_exception(e)
