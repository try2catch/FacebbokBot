import sys
import time

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class facebook_bot():

    def __init__(self, driver, website, username, password, friends=None):
        options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--user-data-dir=/Users/akhileshsingh/Library/Application Support/Google/Chrome/Default')
        options.add_argument('--profile-directory=Default')

        self.driver = webdriver.Chrome(driver, chrome_options=options)
        self.driver.get(website)
        self.friends = friends
        self.login(username=username, password=password)

    def show_exceptions(self, e):
        print(e)
        self.driver.quit()
        sys.exit()

    def isFriend(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'send him a friend request.')))
            return False
        except TimeoutException:
            return True
        except Exception as e:
            self.show_exception(e)

    def login(self, username, password):
        try:
            email_text = self.driver.find_element_by_id('email')
            email_text.send_keys(username)

            pass_text = self.driver.find_element_by_id('pass')
            pass_text.send_keys(password)

            pass_text = self.driver.find_element_by_id('loginbutton')
            pass_text.click()
        except NoSuchElementException as e:
            self.show_exceptions(e)
        except Exception as e:
            self.show_exceptions(e)

    def post_on_wall(self, message=None, media=None):
        url = 'https://www.facebook.com/{}'

        if self.friends:
            if type(self.friends) == str:
                self.driver.get(url.format(self.friends))
                self.post_message(message, media=media)

            elif type(self.friends) == dict:
                for key, value in self.friends.items():
                    self.driver.get(url.format(key))
                    self.post_message(message=message, media=media)

            elif type(self.friends) == list:
                for id in self.friends:
                    self.driver.get(url.format(id))
                    self.post_message(message, media=media)
        else:
            self.post_message(message, media=media)

        self.driver.close()

    def post_media(self, media):
        media_type = type(media)
        if media_type == list:
            for m in media:
                image_box = self.driver.find_element_by_xpath('//input[@type="file"]')
                image_box.send_keys(m)
        elif media_type == str:
            image_box = self.driver.find_element_by_xpath('//input[@type="file"]')
            image_box.send_keys(media)

    def post_message(self, message=None, media=None):
        if self.friends is None:
            post_box = self.driver.find_element_by_tag_name('textarea')
        else:
            if self.isFriend():
                post_box = self.driver.find_element_by_class_name('_1mf')
            else:
                print('Not able to post. Please check friend status.')

        if message:
            post_box.send_keys(message)

        else:
            post_box.click()
            time.sleep(10)

        if media:
            self.post_media(media)

        try:
            if self.friends is None:
                btn_xpath = "//button[@class='_1mf7 _4r1q _4jy0 _4jy3 _4jy1 _51sy selected _42ft']"
            else:
                btn_xpath = "//button[@class='_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft']"

            post_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, btn_xpath)))
            post_btn.click()

        except NoSuchElementException as e:
            self.show_exceptions(e)
        except Exception as e:
            self.show_exceptions(e)

        time.sleep(5)
