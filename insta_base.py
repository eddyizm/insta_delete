# -*- coding: UTF-8 -*-
import os
import pickle
import logging as log
import sys
import time

import pyautogui
from bs4 import BeautifulSoup
from config import Settings
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from random import randrange


def close_shop(driver):
    PID = driver.service.process.pid
    try:
        log.info('closing shop...')
        log.info(f'firefox PID: {PID}')
        driver.close()
        driver.quit()
        driver = None
    except OSError:
        log.exception(OSError.with_traceback())


def screenshot(func_name):
    '''full screenshot to capture errors when debugging'''
    image_name = f'data/{func_name}_{str(time.monotonic())}.png'
    log.info(f'saving screenshot {image_name}')
    pyautogui.screenshot(image_name)


def check_login_status(browser):
    """TODO: Check login in order to use cookies or actually login"""
    pass


def dump_html_to_file(driver):
    ''' used this to debug and find html changes. '''
    checkhtml = BeautifulSoup(driver.page_source, "html.parser")
    with open('data/debug.html', 'w', encoding='utf-8') as w:
        w.write(checkhtml.prettify())


def get_length_of_page(driver):
    return driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")


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
    prefix = 'end' if end_log else 'start'
    log.info(f'{prefix} {get_file_name(file)} session -------------------')


def random_time():
    '''Use this to randomize actions'''
    sleep_time = randrange(5,60)
    log.info(f'sleeping for {sleep_time} seconds...')
    return time.sleep(sleep_time)


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
        not_now_btn = check_for_text('Not Now', driver)
        click_element(driver, not_now_btn, 'Not Now')
    else:
        driver = login_to_site(driver)
    return driver


def check_for_text(search_value: str, browser: webdriver):
    try:
        log.info(f'searching for text: {search_value}')
        ele = browser.find_element(by=By.XPATH, value="//*[contains(text(), '{}')]".format(search_value))
        log.info('text found, returning element')
        return ele
    except Exception as ex:
        log.exception('Error checking for text', exc_info=True)
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


def get_password(driver):
    pass_element = driver.find_element(by=By.XPATH, value="//input[@name='password']")
    log.info(f'found password element: {pass_element}')
    ActionChains(driver).move_to_element(pass_element). \
            click().send_keys(Settings.insta_password).perform()
    random_time()


def get_username(driver):
    user_element = driver.find_element(by=By.XPATH, value="//input[@name='username']")
    log.info(f'found username element: {user_element}')
    ActionChains(driver).move_to_element(user_element). \
        click().send_keys(Settings.insta_username).perform()
    random_time()


def click_login(browser):
    login_button = browser.find_element(by=By.XPATH, value="//*[contains(text(), 'Log in')]")
    log.info(f'found login element: {login_button}')
    ActionChains(browser).move_to_element(login_button).click().perform()
    log.info('login successful...')
    random_time()


def login_to_site(browser) -> webdriver:
    try:
        log.info('logging in')
        browser.get("https://www.instagram.com/accounts/login/")
        get_username(browser)
        get_password(browser)
        click_login(browser)
        save_cookies(browser)
        return browser
    except Exception as err:
        log.info('Errog logging in to site', exc_info=True)
        screenshot('login_to_site')
        sys.exit(1)


# call settings/functions to use in app
Settings = Settings()
handlers = [
    log.StreamHandler(),
    RotatingFileHandler(Settings.app_log, 
        mode='a', maxBytes=5*1024*1024, 
        backupCount=5, encoding=None, delay=0
    )
]
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', handlers = handlers, level=log.INFO)
BASE_DIR = get_working_directory(__file__)
COOKIES = os.path.join(BASE_DIR, 'data/cookies.pkl')
