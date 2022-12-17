# -*- coding: UTF-8 -*-
''' writing a script to automate photo uploads '''
from glob import glob
import os
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector

from random import randrange, shuffle
import pyautogui

import insta_base

log = logging.getLogger(__name__)
pyautogui.FAILSAFE = False


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





def upload_image(browser_object : webdriver, filepath : str):
    try:
        print('finding upload image button')
        insta_base.dump_html_to_file(browser_object)
        browser_object.file_detector = UselessFileDetector()
        if insta_base.check_for_text('Save Your Login Info', browser_object) and insta_base.check_for_text('Turn on Notifications', browser_object):
            browser_object.get(f"https://www.instagram.com/{insta_base.Settings.insta_username}")
        insta_base.stime()
        options_button = browser_object.find_element(by=By.XPATH, 
                            value="//div[@class='q02Nz _0TPg']//*[@aria-label='New Post']")
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


def process_image(browser_object : webdriver, tags : str):
    try:
        time.sleep(60)
        btn = pyautogui.locateOnScreen('screenshots/next.png')
        if btn:
            top = (btn[0] + (btn[2]/2))
            bottom = (btn[1] + (btn[3]/2))
            pyautogui.click(x=top, y=bottom)
            print('found next button, moving to caption screen')
        time.sleep(return_randomtime())
        add_text = browser_object.find_element(by=By.XPATH, value="//textarea[@aria-label='Write a caption…']")
        time.sleep(return_randomtime())
        print('writing caption')
        ActionChains(browser_object).move_to_element(add_text).click().send_keys(tags).perform()
        time.sleep(return_randomtime())
        share_button = browser_object.find_element(by=By.XPATH, value="//button[text()='Share']")
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
    log.info('----------------------------------------------------------------------------------------------------- ')
    log.info('--------------------------------------- new insta_upload session ------------------------------------- ')
    log.info('------------------------------------------------------------------------------------------------------ ')
    attempts = 3
    while attempts > 0:
        attempts = attempts -1
        driver = insta_base.login_to_site()
        if not driver:
            print('attempt failed. trying again')
            time.sleep(return_randomtime())
            continue
        file, tag = get_images(insta_base.Settings.image_path)
        next_driver = upload_image(driver, file)
        if not next_driver:
            print('attempt failed. trying again')
            time.sleep(return_randomtime())
            continue
        combined_tags = f'#{tag} #eddyizm | https://eddyizm.com'
        if process_image(next_driver, combined_tags):
            log.info(f'file posted successfully: {file}')
            os.remove(file)
            break
        else:
            print(f'error posting file.')
            time.sleep(return_randomtime())
            continue

if __name__ == '__main__':
    # time.sleep(randrange(1,3000))
    main()