# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
# crontab for bash script:
# 07 7 * * 1-7 export DISPLAY=:0; /home/eddyizm-hp/Documents/insta_delete/upload.sh  >> /home/eddyizm-hp/HP/upload.log
from bs4 import BeautifulSoup
from datetime import datetime
from glob import glob
from selenium.webdriver.remote.file_detector import UselessFileDetector
import time
import os
import sys
from random import randrange
import pyautogui
# from selenium.webdriver.support.ui import WebDriverWait

''' writing a script to automate photo uploads '''
firefoxPath="env/geckodriver"
logintext = "env/login.txt"
image_path = "/home/eddyizm-hp/HP/images"


''' holding this for testing on windows '''
# def platform_vars():
#     if os.name == 'nt':
#         logintext = "C:\\Users\\eddyizm\\Desktop\\Work\\login.txt"
#         linux = False
#     else:
#         firefoxPath="env/geckodriver"
#         logintext = "env/login.txt"
#         linux = True
#     return logintext, linux, firefoxPath


def dump_html(selenium_driver : str):
    ''' function to out html for inspection when luck is not on  my side '''
    checkhtml = BeautifulSoup(selenium_driver.page_source, "html.parser")
    with open('debug.html', 'w', encoding='utf-8') as w:
        w.write(checkhtml.prettify())


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
    return randrange(13,45)


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
            
        ActionChains(browser).move_to_element(login_button).click().perform()
        time.sleep(return_randomtime())
        # skip over save login credentials screen
        print('login successful, return browser to homepage')
        browser.get("https://www.instagram.com/")
        return browser
    except Exception as err:
        print('error in LoginToSite')
        print (err)        


def upload_image(browser_object : str, filepath : str):
    try:
        print('finding upload image button')
        browser_object.file_detector = UselessFileDetector()
        options_button = browser_object.find_element_by_xpath(
                            "//div[@class='q02Nz _0TPg']//*[@aria-label='New Post']")
        ActionChains(browser_object).move_to_element(options_button).click().perform()
        time.sleep(return_randomtime())
        print('selecting file on local file system')
        pyautogui.write(filepath, interval=0.25) 
        pyautogui.press('return')
        print('file pushed to browser. now to resize and add the tags.')
        time.sleep(return_randomtime())
        return browser_object
    except Exception as ex:
        print('error in upload_image():', ex)
        

def process_image(browser_object : str, tags : str):
    try:
        print('resizing image')
        resize_button = browser_object.find_element_by_xpath(
                            "//button[@class='pHnkA']//span[contains(text(),'Expand')]")
        time.sleep(return_randomtime())
        ActionChains(browser_object).move_to_element(resize_button).click().perform()
        time.sleep(return_randomtime())
        print('moving to caption screen')
        next_button = browser_object.find_element_by_xpath(
                        "//button[text()='Next']")
        time.sleep(return_randomtime())
        ActionChains(browser_object).move_to_element(next_button).click().perform()
        time.sleep(return_randomtime())
        # dump_html(browser_object)
        add_text = browser_object.find_element_by_xpath(
                        "//textarea[@aria-label='Write a caption…']")
        time.sleep(return_randomtime())
        print('writing caption')
        ActionChains(browser_object).move_to_element(add_text).click().send_keys(tags).perform()
        time.sleep(return_randomtime())
        share_button = browser_object.find_element_by_xpath(
                        "//button[text()='Share']")
        time.sleep(return_randomtime())
        ActionChains(browser_object).move_to_element(share_button).click().perform()
        time.sleep(return_randomtime())
        print('post succesful!')
        browser_object.close()
        return True
    except Exception as ex:
        print('error in process_image():', ex)
        browser_object.close()
        return False


def main():
    driver = login_to_site()
    file, tag = get_images(image_path)
    next_driver = upload_image(driver, file)
    combined_tags = f'#{tag} #eddyizm'
    if process_image(next_driver, combined_tags):
        print(f'file posted successfully,\nnow delete the image from local disk: {file}')
        os.remove(file)
    else:
        print(f'error posting file. check the logs') 


if __name__ == '__main__':
    time.sleep(randrange(1,3600))
    main()