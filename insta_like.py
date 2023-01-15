# -*- coding: UTF-8 -*-
''' writing a script to like posts in my thread '''
import logging
import pickle

from selenium.webdriver.common.by import By

import insta_base as ib
import insta_delete as id

log = logging.getLogger(__name__)


def find_likes(browser):
    try: 
        log.info('finding like svg element')
        btn = browser.find_elements(by=By.XPATH, value="//button[@class='_abl-']//*[local-name()='svg' and @aria-label='Like']")
        log.info(f'found {len(btn)} btns')
        return btn
    except Exception as ex:
        log.info('like element not found', exc_info=True)
        return None


def find_like(browser):
    try: 
        log.info('finding like svg element')
        btn = browser.find_elements(by=By.XPATH, value="//button[@class='_abl-']//*[local-name()='svg' and @aria-label='Like']")[1]
        log.info(f'found btn: {btn}')
        return btn
    except Exception as ex:
        log.info('like element not found', exc_info=True)
        return None


def delete_with_cookies():
    driver = ib.get_driver()
    driver.get("https://www.instagram.com/")
    ib.load_cookies(driver)
    ib.random_time()
    id.delete_posts(browser=driver)


def inspect_cookies():
    cookies = pickle.load(open("data/cookies.pkl", "rb"))
    log.info('loading cookies')
    for cookie in cookies:
        log.info(cookie)


def like_post(driver):
    like_btn = find_like(driver)
    if like_btn and like_btn.is_displayed():
        log.info(f'is like btn displayed? : {like_btn.is_displayed()}')
        log.info('scrolling into view')
        like_btn.location_once_scrolled_into_view
        log.info(f'is enabled: {like_btn.is_enabled()}')
        ib.click_element(driver, like_btn)
    else:
        log.info('post not liked.')


def like_multiple_posts(driver, posts_to_like:int = 1):
    log.info('liking multiple posts')
    while (posts_to_like > 0):
        like_post(driver)
        driver.get('https://www.instagram.com/')
        ib.random_time()
        posts_to_like -= 1


def main():
    ib.start_end_log(__file__)
    driver = ib.login_with_cookies()
    like_multiple_posts(driver, posts_to_like=4)
    ib.save_cookies(driver)
    driver.close()


if __name__ == "__main__":
    main()
    ib.start_end_log(__file__, end_log=True)
