# -*- coding: UTF-8 -*-
''' writing a script to automate photo uploads '''
from glob import glob
import os
import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector

from random import shuffle
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


def upload_image(browser_object : webdriver, filepath : str):
    try:
        log.info('finding upload image button')
        insta_base.stime(True)
        browser_object.file_detector = UselessFileDetector()
        if insta_base.check_for_text('Save Your Login Info', browser_object) and insta_base.check_for_text('Turn on Notifications', browser_object):
            browser_object.get(f"https://www.instagram.com/")
        
        new_post_option = browser_object.find_element(by=By.XPATH,
                            value="//*[local-name()='svg' and @aria-label='New post']")
        log.info('found new post option')
        ActionChains(browser_object).move_to_element(new_post_option).click().perform()
        
        upload_button = browser_object.find_element(by=By.XPATH,
                            value="//button[text()='Select from computer']")
        log.info('found upload button')
        ActionChains(browser_object).move_to_element(upload_button).click().perform()
        log.info('selecting file on local file system')
        # browser_object.save_screenshot(os.path.join(insta_base.BASE_DIR,'selectingfile.png'))
        pyautogui.write(filepath, interval=0.25)
        pyautogui.press('return')
        pyautogui.press('enter')
        # browser_object.save_screenshot(os.path.join(insta_base.BASE_DIR, 'lookingforOpenBTN.png'))
        # open_png = os.path.join(insta_base.BASE_DIR, 'screenshots/open.png')
        # btn = pyautogui.locateOnScreen(open_png)
        # time.sleep(30)
        # if btn:
        #     top = (btn[0] + (btn[2]/2))
        #     bottom = (btn[1] + (btn[3]/2))
        #     pyautogui.click(x=top, y=bottom)
        #     log.info('file pushed to browser... add the tags.')
        # else:
        #     log.info('open button not found')
        #     return None
        log.info('file pushed to browser...returning browser object')
        return browser_object
    except Exception as ex:
        browser_object.quit()
        log.error('error in upload_image():', exc_info=True)


def process_image(browser_object : webdriver, tags : str):
    try:
        log.info('starting process_image')
        # next_png = os.path.join(insta_base.BASE_DIR, 'screenshots/next.png')
        # btn = pyautogui.locateOnScreen(next_png)
        btn = browser_object.find_element(by=By.XPATH,
                            value="//button[.='Next']")
        if btn:
            # top = (btn[0] + (btn[2]/2))
            # bottom = (btn[1] + (btn[3]/2))
            log.info('found next button')
            ActionChains(browser_object).move_to_element(btn).click().perform()
        else:
            log.warn('Next button not found...fail!')
            return False
        btn = browser_object.find_element(by=By.XPATH,
                            value="//button[.='Next']")
        if btn:
            ActionChains(browser_object).move_to_element(btn).click().perform()
            log.info('found next button, moving to caption screen')
        else:
            log.warn('Next button not found...fail!')
            return False            
        browser_object.implicitly_wait(10)
        add_text = browser_object.find_element(by=By.XPATH, value="//*[local-name()='div' and @aria-label='Write a caption...']")
        insta_base.stime()
        log.info('writing caption')
        ActionChains(browser_object).move_to_element(add_text).click().send_keys(tags).perform()
        insta_base.stime(True)
        share_button = browser_object.find_element(by=By.XPATH, value="//button[.='Share']")
        insta_base.stime()
        ActionChains(browser_object).move_to_element(share_button).click().perform()
        insta_base.stime(True)
        log.info('post successful!')
        browser_object.quit()
        return True
    except Exception as ex:
        log.error('error in process_image():',  exc_info=True)
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
            log.info('attempt failed. trying again')
            insta_base.stime(True)
            continue
        file, tag = get_images(insta_base.Settings.image_path)
        next_driver = upload_image(driver, file)
        if not next_driver:
            log.info('attempt failed. trying again')
            insta_base.stime(True)
            continue
        combined_tags = f'#{tag} #eddyizm | https://eddyizm.com'
        if process_image(next_driver, combined_tags):
            log.info(f'file posted successfully: {file}')
            os.remove(file)
            break
        else:
            log.info(f'error posting file.')
            insta_base.stime(True)
            continue


if __name__ == '__main__':
    # time.sleep(randrange(1,3000))
    main()