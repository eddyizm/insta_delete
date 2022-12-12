# -*- coding: UTF-8 -*-
''' writing a script to automate photo uploads '''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.file_detector import UselessFileDetector
from bs4 import BeautifulSoup
from datetime import datetime
from glob import glob
import time
import os
from random import randrange, shuffle
import pyautogui
from insta_delete import get_keys
# import twitter bot to upload image there as well
import sys
sys.path.append(r'C:\Users\eddyizm\Source\repo\twitterbot/')
from post_image import tweet_photos, tweepy_creds, search_twtr, fave_tweet
pyautogui.FAILSAFE = False


if os.name == 'nt':
    settings = get_keys()
    logintext = r'C:\Users\eddyizm\Desktop\Work\login.txt'  # TODO replace logintext with login/pass
    insta_username = settings['instagram']['login']
    insta_password = settings['instagram']['pass']
    log_path = settings['windows']['log_path']
    app_log = settings['windows']['app_log']
    firefoxPath= settings['windows']['firefoxPath']
    desk_profile = settings['windows']['profile_path']
    image_path = settings['windows']['image_path']
else:
    firefoxPath="env/geckodriver"
    logintext = "env/login.txt"
    image_path = "/home/eddyizm-hp/HP/images"
    desk_profile = r'/home/eddyizm-hp/.mozilla/firefox/69f6brir.default'


def dump_html(selenium_driver : str):
    ''' function to out html for inspection when luck is not on  my side '''
    checkhtml = BeautifulSoup(selenium_driver.page_source, "html.parser")
    with open('debug.html', 'w', encoding='utf-8') as w:
        w.write(checkhtml.prettify())


def get_images(folder : str):
    ''' get a list of image from a folder recursively and randomize before returning one for posting '''
    folders = glob(folder+'/**/*.jpg', recursive=True)
    shuffle(folders) 
    fullpath = ''
    for filename in folders:
        if os.path.isfile(filename):
            fullpath = filename
            break # get first directory if it exists
    foldertag = os.path.basename(os.path.dirname(fullpath))
    return fullpath, foldertag


def return_randomtime():
    return randrange(25,60)


def login_to_site():
    try:
        print ('logging in as mobile device')
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user_agent = "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
        profile = webdriver.FirefoxProfile(desk_profile)
        profile.set_preference("general.useragent.override", user_agent)
        time.sleep(return_randomtime())
        browser = webdriver.Firefox(firefox_profile = profile, executable_path=firefoxPath, service_log_path='env/geckodriver.log')
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
        time.sleep(return_randomtime())
        return browser
    except Exception as err:
        print('error in LoginToSite')
        print (err)
        browser.quit()


def upload_image(browser_object : str, filepath : str):
    try:
        print('finding upload image button')
        browser_object.file_detector = UselessFileDetector()
        options_button = browser_object.find_element_by_xpath(
                            "//div[@class='q02Nz _0TPg']//*[@aria-label='New Post']")
        ActionChains(browser_object).move_to_element(options_button).click().perform()
        time.sleep(return_randomtime())
        print('selecting file on local file system')
        # browser_object.save_screenshot("selectingfile.png")
        pyautogui.write(filepath, interval=0.25)
        pyautogui.press('return')
        pyautogui.press('enter')
        # browser_object.save_screenshot("lookingforOpenBTN.png")
        btn = pyautogui.locateOnScreen('screenshots/open.png')
        if btn:
            top = (btn[0] + (btn[2]/2))
            bottom = (btn[1] + (btn[3]/2))
            pyautogui.click(x=top, y=bottom)
            print('file pushed to browser... add the tags.')
        time.sleep(30)
        return browser_object
    except Exception as ex:
        browser_object.quit()
        print('error in upload_image():', ex)


def process_image(browser_object : str, tags : str):
    try:
        # dump_html(browser_object)
        time.sleep(60)
        btn = pyautogui.locateOnScreen('screenshots/next.png')
        if btn:
            top = (btn[0] + (btn[2]/2))
            bottom = (btn[1] + (btn[3]/2))
            pyautogui.click(x=top, y=bottom)
            print('found next button, moving to caption screen')
        time.sleep(return_randomtime())
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
        browser_object.quit()
        return True
    except Exception as ex:
        print('error in process_image():', ex)
        browser_object.quit()
        return False


def main():
    attempts = 3
    while attempts > 0:
        attempts = attempts -1
        driver = login_to_site()
        if not driver:
            print('attempt failed. trying again')
            time.sleep(return_randomtime())
            continue
        file, tag = get_images(image_path)
        next_driver = upload_image(driver, file)
        if not next_driver:
            print('attempt failed. trying again')
            time.sleep(return_randomtime())
            continue
        combined_tags = f'#{tag} #eddyizm | https://eddyizm.com'
        if process_image(next_driver, combined_tags):
            print(f'file posted successfully,\nnow going to post to twitterbot: {file}')
            twitter_api = tweepy_creds()
            tweet_photos(twitter_api, file, tag)
            search_results = search_twtr(twitter_api, tag)
            fave_tweet(twitter_api, search_results)
            # os.remove(file)
            break
        else:
            print(f'error posting file.')
            time.sleep(return_randomtime())
            continue

if __name__ == '__main__':
    time.sleep(randrange(1,3000))
    main()