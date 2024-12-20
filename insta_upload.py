# -*- coding: UTF-8 -*-
''' writing a script to automate photo uploads '''
import os
import logging
from glob import glob
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector
from sys import exit
from random import shuffle

import insta_base as ib
import caption

log = logging.getLogger(__name__)


def get_image(folder: str):
    ''' get a list of image from a folder recursively and randomize before returning one for posting '''
    folders = glob(folder + '/**/*.jpg', recursive=True)
    shuffle(folders)
    fullpath = ''
    for filename in folders:
        if os.path.isfile(filename):
            fullpath = filename
            break  # get first directory if it exists
    return fullpath.replace('/', '\\')


def select_local_file(full_file_path, osname):
    log.info(f'selecting file on local file system: {full_file_path}')
    if osname == 'DARWIN':
        import pyobjc.applescript
        """Uses AppleScript to open the file selection dialog and simulate choosing the file"""
        log.info(f'selecting file on local file system: {full_file_path}')
        
        # Construct AppleScript code
        script = f"""tell application "Finder"
            activate
            set theFile to POSIX file "{full_file_path}" as alias
            open selection of theFile
        end tell"""
        # Run the AppleScript
        try:
            ascript = pyobjc.applescript.NSAppleScript(source=script)
            ascript.run()
            log.info('File selection dialog opened.')
        except Exception as e:
            log.error(f'Error running AppleScript: {e}')
    else:
        """pyautogui actions to select file and close pop up"""
        import pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.write(full_file_path)
        ib.random_time()
        log.info('tabbing over')
        pyautogui.press('tab')
        pyautogui.press('tab')
        ib.random_time()
        pyautogui.press('enter')
        log.info('window explorer tabbed and hit entered to close')


def find_upload_button(browser):
    upload_button = browser.find_element(
        by=By.XPATH,
        value="//button[text()='Select from computer']"
    )
    log.info('found select from computer button')
    ib.click_element(browser, upload_button, 'upload button')
    ib.random_time()


def find_new_post(browser):
    log.info('locating new post option')
    new_post_option = browser.find_element(
        by=By.XPATH,
        value="//*[local-name()='svg' and @aria-label='New post']"
    )
    log.info('found new post option')
    ib.click_element(browser, new_post_option, 'new post option')
    ib.random_time()
    new_post_option = browser.find_element(
        by=By.XPATH,
        value="//span[contains(text(), 'Post')]"
    )
    log.info('second post option')
    ib.click_element(browser, new_post_option, 'second post option')
    ib.random_time()


def upload_image(browser: webdriver, filepath: str, osname: str):
    try:
        log.info('finding upload image button')
        ib.random_time()
        browser.file_detector = UselessFileDetector()
        ib.bypass_notification_prompt(browser)
        find_new_post(browser)
        find_upload_button(browser)
        select_local_file(filepath, osname)
    except Exception as ex:
        browser.quit()
        log.error('error in upload_image():', exc_info=True)


def find_next_button(browser):
    '''find delete button and click!'''
    log.info('finding next button...')
    ib.random_time()
    next = browser.find_element(by=By.XPATH,
                                value="//div[@role='button' and text()='Next']")
    log.info('found next button')                            
    ib.click_element(browser, next, 'next')


def select_original_crop(browser):
    '''resizing image using select crop button to original'''
    log.info('finding select crop button...')
    ib.random_time()
    crop_button = browser.find_element(
        by=By.XPATH,
        value="//*[local-name()='svg' and @aria-label='Select crop']"
    )
    log.info('found select crop button')   
    ib.click_element(browser, crop_button, 'crop_button')
    ib.random_time()
    original = browser.find_element(
        by=By.XPATH,
        value="//span[contains(text(), 'Original')]"
    )
    log.info('found select original button')
    ib.click_element(browser, original, 'original')


def share_image(browser):
    log.info('locating share button')
    share_button = browser.find_element(by=By.XPATH, value="//div[@role='button' and text()='Share']")
    log.info('sharing post')
    ActionChains(browser).move_to_element(share_button).click().perform()
    ib.random_time()
    log.info('post successful!')


def add_captions(browser, caption):
    add_text = browser.find_elements(by=By.XPATH, value="//*[local-name()='div' and @aria-label='Write a caption...']")[0]
    log.info('writing caption')
    ActionChains(browser).move_to_element(add_text).click().send_keys(caption).perform()
    ib.random_time()


def process_image(browser_object: webdriver, tags: str):
    try:
        log.info('starting process_image')
        select_original_crop(browser_object)
        find_next_button(browser_object)
        ib.random_time()
        find_next_button(browser_object)
        add_captions(browser=browser_object, caption=tags)
        share_image(browser_object)
        ib.save_cookies(browser_object)
        return True
    except Exception as ex:
        log.error('error in process_image():', exc_info=True)
        browser_object.quit()
        return False


def main():
    ib.start_end_log(__file__)
    driver = ib.login_with_cookies()
    try:
        file = get_image(ib.Settings.image_path)
        tag = caption.get_caption(file)
        upload_image(driver, file, ib.Settings.osname)
        if process_image(driver, tag):
            ib.close_shop(driver)
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
