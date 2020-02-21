# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
from glob import glob
import time
import os
import sys
from random import randrange

''' writing a script to automate photo uploads '''
firefoxPath="env/geckodriver"
logintext = "env/login.txt"
image_path = "/home/eddyizm-hp/HP/images"

def platform_vars():
    if os.name == 'nt':
        # log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
        logintext = "C:\\Users\\eddyizm\\Desktop\\Work\\login.txt"
        linux = False
    else:
        firefoxPath="env/geckodriver"
        logintext = "env/login.txt"
        # log_path = 'env/media_urls.txt'
        linux = True
    return logintext, linux, firefoxPath


def get_images(folder : str):
    folders = glob(folder+'/**/*.jpg', recursive=True)
    fullpath = ''
    for filename in folders:
        if os.path.isfile(filename):
            fullpath = filename
            break # get first directory if it exists
    foldertag = os.path.basename(os.path.dirname(fullpath))
    return fullpath, foldertag

def return_randomtime():
    return randrange(35)


def login_to_site():
    try:
        print ('logging in as mobile device')
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile() 
        profile.set_preference("general.useragent.override", user_agent)
        browser = webdriver.Firefox(firefox_profile = profile, executable_path=firefoxPath)
        browser.set_window_size(360,640)
        browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(return_randomtime())
        f = open (logintext, 'r')
        login = f.read().splitlines()
        f.close()
        insta_username = login[0]
        insta_password = login[1]
        eUser = browser.find_elements_by_xpath(
            "//input[@name='username']")
        time.sleep(return_randomtime())
        ActionChains(browser).move_to_element(eUser[0]). \
            click().send_keys(insta_username).perform()
        time.sleep(return_randomtime())
        ePass = browser.find_elements_by_xpath(
            "//input[@name='password']")
        time.sleep(return_randomtime())
        ActionChains(browser).move_to_element(ePass[0]). \
            click().send_keys(insta_password).perform()

        time.sleep(return_randomtime())
        login_button = browser.find_element_by_xpath(
            "//*[contains(text(), 'Log In')]")
            #"//button[text()='Log In']")
            #"//form/span/button[text()='Log In']")
                     
        ActionChains(browser).move_to_element(login_button).click().perform()
        time.sleep(return_randomtime())
        return browser
    except Exception as err:
        print (err)        





if __name__ == '__main__':
    file, tag = get_images(image_path)
    print(file, tag)
    pass