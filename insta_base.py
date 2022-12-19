# -*- coding: UTF-8 -*-
import json
import logging as log
import os
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from models import Settings

CONFIG = r"C:\Users\eddyizm\HP\config.json"


def get_working_directory(_file):
    return os.path.dirname(_file)


def dump_html_to_file(driver):
    ''' used this to debug and find html changes. '''
    checkhtml = BeautifulSoup(driver.page_source, "html.parser")
    with open('debug.html', 'w', encoding='utf-8') as w:
        w.write(checkhtml.prettify())


def stime():
    '''Use this to randomize actions'''
    return time.sleep(5)


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
        
        
def login_to_site():
    try:
        log.info('logging in as mobile device to delete')
        # user_agent = "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
        options=Options()
        options.set_preference('profile', Settings.profile_path)
        service = Service(Settings.firefox_path)
        browser = webdriver.Firefox(service=service, options=options)
        browser.set_window_size(1200,927)
        browser.get("https://www.instagram.com/accounts/login/")
        stime()
        eUser = browser.find_element(by=By.XPATH, value="//input[@name='username']")
        log.info(f'found username element: {eUser}')
        stime()
        ActionChains(browser).move_to_element(eUser). \
            click().send_keys(Settings.insta_username).perform()
        stime()
        ePass = browser.find_element(by=By.XPATH, value="//input[@name='password']")
        log.info(f'found password element: {ePass}')
        stime()
        ActionChains(browser).move_to_element(ePass). \
            click().send_keys(Settings.insta_password).perform()

        stime()
        login_button = browser.find_element(by=By.XPATH, value="//*[contains(text(), 'Log in')]")
            #"//button[text()='Log In']")
            #"//form/span/button[text()='Log In']")
        log.info(f'found login element: {login_button}')
        ActionChains(browser).move_to_element(login_button).click().perform()
        stime()
        log.info('login successful...')
        return browser
    except Exception as err:
        log.info('Errog logging in to site', exc_info=True)
        # browser.close()
        sys.exit(1)

# call settings/functions to use in app
Settings = get_settings()
handlers = [log.FileHandler(Settings.app_log), log.StreamHandler()]
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', handlers = handlers, level=log.INFO)
BASE_DIR = get_working_directory(__file__)