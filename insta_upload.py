# -*- coding: UTF-8 -*-
''' writing a script to automate photo uploads '''
from glob import glob
import os
import logging


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector

from sys import exit
from random import shuffle
import pyautogui

import insta_base as ib

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
    foldertag = f'#{os.path.basename(os.path.dirname(fullpath))} #eddyizm | https://eddyizm.com'
    return fullpath, foldertag


def select_local_file(full_file_path):
    """pyautogui actions to select file and close pop up"""
    log.info(f'selecting file on local file system: {full_file_path}')
    pyautogui.write(full_file_path)
    ib.stime
    pyautogui.press('tab')
    pyautogui.press('tab')
    ib.stime
    pyautogui.press('enter')
    log.info('window explorer tabbed and hit entered to close')


def upload_image(browser : webdriver, filepath : str):
    try:
        log.info('finding upload image button')
        ib.stime(True)
        browser.file_detector = UselessFileDetector()
        new_post_option = browser.find_element(by=By.XPATH,
                            value="//*[local-name()='svg' and @aria-label='New post']")
        log.info('found new post option')
        ActionChains(browser).move_to_element(new_post_option).click().perform()
        ib.stime(True)
        upload_button = browser.find_element(by=By.XPATH,
                            value="//button[text()='Select from computer']")
        log.info('found select from computer button')
        ib.stime()
        ActionChains(browser).move_to_element(upload_button).click().perform()
        ib.stime(True)
        select_local_file(filepath)
        ib.stime()
    except Exception as ex:
        browser.quit()
        log.error('error in upload_image():', exc_info=True)


def process_image(browser_object : webdriver, tags : str):
    try:
        log.info('starting process_image')
        ib.stime()
        log.info('looking for next button')
        btn = browser_object.find_element(by=By.XPATH,
                            value="//button[.='Next']")
        ib.stime(True)
        if btn:
            log.info('found next button')
            ActionChains(browser_object).move_to_element(btn).click().perform()
        else:
            log.warn('Next button not found...fail!')
            return False
        ib.stime()
        btn = browser_object.find_element(by=By.XPATH,
                            value="//button[.='Next']")
        ib.stime(True)
        if btn:
            ActionChains(browser_object).move_to_element(btn).click().perform()
            log.info('found next button, moving to caption screen')
        else:
            log.warn('Next button not found...fail!')
            return False            
        browser_object.implicitly_wait(10)
        add_text = browser_object.find_elements(by=By.XPATH, value="//*[local-name()='div' and @aria-label='Write a caption...']")[0]
        ib.stime()
        log.info('writing caption')
        ActionChains(browser_object).move_to_element(add_text).click().send_keys(tags).perform()
        ib.stime(True)
        log.info('locating share button')
        share_button = browser_object.find_element(by=By.XPATH, value="//button[.='Share']")
        ib.stime()
        log.info('sharing post')
        ActionChains(browser_object).move_to_element(share_button).click().perform()
        ib.stime(True)
        log.info('post successful!')
        ib.save_cookies(browser_object)
        return True
    except Exception as ex:
        log.error('error in process_image():',  exc_info=True)
        browser_object.quit()
        return False


def main():
    ib.start_end_log(__file__)
    driver = ib.login_with_cookies()
    try:
        file, tag = get_images(ib.Settings.image_path)
        upload_image(driver, file)
        if process_image(driver, tag):
            driver.quit()
            os.remove(file)
            log.info(f'file posted successfully and deleted: {file}')
    except Exception as ex:
        log.info(f'error posting file.', exc_info=True)
        ib.start_end_log(__file__, True)
        exit(1)


if __name__ == '__main__':
    main()
    ib.start_end_log(__file__, True)
    exit(0)