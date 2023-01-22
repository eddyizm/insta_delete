# -*- coding: UTF-8 -*-
''' writing a script to automate photo uploads '''
import os
import pyautogui
import logging
from glob import glob
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector
from sys import exit
from random import shuffle

import insta_base as ib
from .caption import get_caption

log = logging.getLogger(__name__)
pyautogui.FAILSAFE = False


def get_image(folder : str):
    ''' get a list of image from a folder recursively and randomize before returning one for posting '''
    folders = glob(folder+'/**/*.jpg', recursive=True)
    shuffle(folders)
    fullpath = ''
    for filename in folders:
        if os.path.isfile(filename):
            fullpath = filename
            break # get first directory if it exists
    return fullpath


def select_local_file(full_file_path):
    """pyautogui actions to select file and close pop up"""
    log.info(f'selecting file on local file system: {full_file_path}')
    pyautogui.write(full_file_path)
    ib.random_time()
    pyautogui.press('tab')
    pyautogui.press('tab')
    ib.random_time()
    pyautogui.press('enter')
    log.info('window explorer tabbed and hit entered to close')


def find_upload_button(browser):
    upload_button = browser.find_element(by=By.XPATH,
                        value="//button[text()='Select from computer']")
    log.info('found select from computer button')
    ib.click_element(browser, upload_button, 'upload button')
    ib.random_time()
    

def find_new_post(browser):
    log.info('locating new post option')
    new_post_option = browser.find_element(by=By.XPATH,
                        value="//*[local-name()='svg' and @aria-label='New post']")
    log.info('found new post option')
    ib.click_element(browser, new_post_option, 'new post option')
    ib.random_time()


def upload_image(browser : webdriver, filepath : str):
    try:
        log.info('finding upload image button')
        ib.random_time()
        browser.file_detector = UselessFileDetector()
        find_new_post(browser)
        find_upload_button(browser)
        select_local_file(filepath)
    except Exception as ex:
        browser.quit()
        log.error('error in upload_image():', exc_info=True)


def find_next_button(browser):
    '''find delete button and click!'''
    log.info(f'finding next button...')
    ib.random_time()
    next = browser.find_element(by=By.XPATH,
                            value="//button[.='Next']")
    log.info('found next button')                            
    ib.click_element(browser, next, 'next')


def process_image(browser_object : webdriver, tags : str):
    try:
        log.info('starting process_image')
        find_next_button(browser_object)
        ib.random_time()
        find_next_button(browser_object)
        add_text = browser_object.find_elements(by=By.XPATH, value="//*[local-name()='div' and @aria-label='Write a caption...']")[0]
        log.info('writing caption')
        ActionChains(browser_object).move_to_element(add_text).click().send_keys(tags).perform()
        ib.random_time()
        log.info('locating share button')
        share_button = browser_object.find_element(by=By.XPATH, value="//button[.='Share']")
        log.info('sharing post')
        ActionChains(browser_object).move_to_element(share_button).click().perform()
        ib.random_time()
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
        file = get_image(ib.Settings.image_path)
        tag = get_caption(file)
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