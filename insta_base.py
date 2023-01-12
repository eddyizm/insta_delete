# -*- coding: UTF-8 -*-
import json
import logging as log
import pickle
import os
import sys
from random import randrange
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from models import Settings

CONFIG = r"C:\Users\eddyizm\HP\config.json"


def check_login_status(browser):
    """TODO: Check login in order to use cookies or actually login"""
    pass


def scroll_home(browser) -> bool:
    try:
        log.info('scrolling home')
        ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.HOME).key_up(Keys.CONTROL).perform()
        return True
    except:
        log.info('error scrolling home', exc_info=True)
        return False


def scroll(browser) -> webdriver:
    log.info('scrolling full page')
    return browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")


def load_cookies(browser):
    cookies = pickle.load(open(COOKIES, "rb"))
    log.info('loading cookies')
    for cookie in cookies:
        browser.add_cookie(cookie)
    return browser


def save_cookies(browser):
    log.info('saving cookies')
    pickle.dump( browser.get_cookies() , open(COOKIES,"wb"))


def get_file_name(_file):
    return os.path.basename(_file)


def get_working_directory(_file):
    return os.path.dirname(_file)


def start_end_log(file, end_log=False):
    log.info('-----------------------------------------------------------')
    prefix = 'end' if end_log else 'start'
    log.info(f'{prefix} {get_file_name(file)} session -------------------')
    log.info('-----------------------------------------------------------')


def dump_html_to_file(driver):
    ''' used this to debug and find html changes. '''
    checkhtml = BeautifulSoup(driver.page_source, "html.parser")
    with open('debug.html', 'w', encoding='utf-8') as w:
        w.write(checkhtml.prettify())


def stime(randomize: bool = False):
    '''Use this to randomize actions'''
    if randomize:
        return time.sleep(randrange(10,60)) #TODO depreciate the boolean, just make it random every time
    return time.sleep(randrange(5,60))


def click_element(browser, elem, elem_name=None):
    try:
        _name = elem if elem_name is None else elem_name
        log.info(f'clicking element: {_name}')
        ActionChains(browser).move_to_element(elem).click().perform()
        log.info(f'{_name} clicked successfully!')
    except MoveTargetOutOfBoundsException:
        log.info('Error click_element', exc_info=True)
        

def login_with_cookies() -> webdriver:
    driver = get_driver()
    driver.get("https://www.instagram.com/")
    load_cookies(driver)
    
    driver.get("https://www.instagram.com/")
    if check_for_text('Turn on Notifications', driver):
        not_now_btn = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Not Now')]")
        click_element(driver, not_now_btn)
    else:
        driver = login_to_site(driver)
    return driver


def get_settings() -> Settings:
    ''' get settings and return populated model '''
    settings = get_keys()
    return Settings(settings['instagram']['login'],
        settings['instagram']['pass'],
        settings['windows']['log_path'],
        settings['windows']['app_log'],
        settings['windows']['firefox_path'],
        settings['windows']['profile_path'],
        settings['windows']['image_path']
        )


def get_keys():
    with open(CONFIG, 'r') as myfile:
        keys = myfile.read()
        return json.loads(keys)


def check_for_text(search_value: str, browser: webdriver):
    try:
        log.info(f'searching for text: {search_value}')
        return search_value.lower() in browser.page_source.lower()
    except Exception as ex:
        return None
        

def get_driver() -> webdriver:        
    log.info('getting webdriver')
    options=Options()
    options.set_preference('profile', Settings.profile_path)
    service = Service(Settings.firefox_path)
    browser = webdriver.Firefox(service=service, options=options)
    browser.set_window_size(1200,800)
    browser.implicitly_wait(15)
    return browser


def login_to_site(browser) -> webdriver:
    try:
        log.info('logging in')
        browser.get("https://www.instagram.com/accounts/login/")
        eUser = browser.find_element(by=By.XPATH, value="//input[@name='username']")
        log.info(f'found username element: {eUser}')
        ActionChains(browser).move_to_element(eUser). \
            click().send_keys(Settings.insta_username).perform()
        ePass = browser.find_element(by=By.XPATH, value="//input[@name='password']")
        log.info(f'found password element: {ePass}')
        ActionChains(browser).move_to_element(ePass). \
            click().send_keys(Settings.insta_password).perform()
        login_button = browser.find_element(by=By.XPATH, value="//*[contains(text(), 'Log in')]")
        log.info(f'found login element: {login_button}')
        ActionChains(browser).move_to_element(login_button).click().perform()
        log.info('login successful...')
        save_cookies(browser)
        return browser
    except Exception as err:
        log.info('Errog logging in to site', exc_info=True)
        sys.exit(1)

# call settings/functions to use in app
Settings = get_settings()
handlers = [log.FileHandler(Settings.app_log), log.StreamHandler()]
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', handlers = handlers, level=log.INFO)
BASE_DIR = get_working_directory(__file__)
COOKIES = os.path.join(BASE_DIR, 'data/cookies.pkl')