# -*- coding: UTF-8 -*-
import os
import logging
import sys

from bs4 import BeautifulSoup, SoupStrainer
from selenium.webdriver.common.by import By

import insta_base as ib

log = logging.getLogger(__name__)


def open_archive():
    """open and read archive file of filtered urls"""
    new_file = []
    with open(ib.Settings.log_path, 'r', encoding= 'utf-8') as g:
        lines = g.read().splitlines()
        for l in lines:
            if l.startswith('https://www.instagram.com/p/'):
                new_file.append(l)
        return new_file


def write_to_archive(log, data):
    """write collected urls to file"""
    with open(log, 'w', encoding= 'utf-8') as f:
        for d in data:
            if d.startswith('https://www.instagram.com/'):
                f.write(str(d)+'\n')
            else:
                f.write('https://www.instagram.com'+str(d)+'\n')


def parse_href(data):
    url_list = []
    for link in BeautifulSoup(data, "html.parser", parse_only=SoupStrainer('a') ):
        if link.has_attr('href'):
            t = link.get('href')
            if t is not None:
                url_list.append(t)
    return url_list


def find_delete_button(browser):
    '''find delete button and click!'''
    log.info(f'finding delete button...')
    ib.random_time()
    delete = browser.find_element(by=By.XPATH, value="//button[text()='Delete']")
    ib.click_element(browser, delete, 'delete')


def scrape_current_post_count(browser) -> int:
    log.info('Getting current post count')
    post_count = -1
    try:
        browser.get(f"https://www.instagram.com/{ib.Settings.insta_username}")
        ib.random_time()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        spans = soup.body.find('div', attrs={'class': '_aacl _aacp _aacu _aacx _aad6 _aade'})
        span = spans.find('span')
        post_count = int(span.text)
        log.info(f'post count: {post_count}')
        return post_count
    except ValueError as err:
        log.info('profile_post_min :ERROR:')
        log.info(err)
        return post_count


def scroll_loop(browser, length, count = 0, match = False):
    # TODO add date posted scraping along with post count.
    while(match==False):
        last_count = length
        ib.random_time()
        log.info(f'scrolling {count}...')
        len_of_page = ib.get_length_of_page(browser)
        count += 1
        # added count to ensure only older images get picked up.
        if (last_count==len_of_page) and (count > 25):
            match=True
    log.info('scrolled down: '+str(count)+' times!')


def scroll_to_end(browser):
    log.info('scrolling profile to get more urls')
    try:
        browser.get(f"https://www.instagram.com/{ib.Settings.insta_username}")
        len_of_page = ib.get_length_of_page(browser)
        scroll_loop(browser, len_of_page)
    except Exception as err:
        log.info('error scrolling to end', exc_info=True)
    return browser.page_source


def delete_post(browser, url, url_list):
    log.info(f'finding 3 dot options...')
    more_options = browser.find_elements(by=By.XPATH, value="//*[local-name()='svg' and @aria-label='More options']")[1]
    ib.random_time()
    ib.click_element(browser, more_options, 'more options')
    find_delete_button(browser)
    find_delete_button(browser)
    url_list.append(url)
    log.info('POST DELETED: ' + url)
    return url_list


def delete_loop(browser, counter, urls) -> list:
    log.info('DELETING POSTS!')
    deleted_urls = []
    while (counter > -1):
        log.info(f'getting new url: {urls[counter]}')
        browser.get(urls[counter])
        ib.random_time()
        if ("Sorry, this page isn't available." in browser.page_source):
            deleted_urls.append(urls[counter])
            log.info('URL not found, removing from list')
            counter -= 1
        else:
            deleted_urls = delete_post(browser, urls[counter], deleted_urls)
            counter -= 1
    return [x for x in urls if x not in deleted_urls]


def delete_posts(browser):
        new_file = open_archive()
        counter = (len(new_file) - 1) if (10 >= len(new_file)) else 10
        log.info('number of posts to delete: '+str(counter))
        try:
            remaining_urls = delete_loop(browser, counter, new_file) # [x for x in new_file if x not in deleted_urls]
            log.info('while loop done and exited successfully')
            write_to_archive(ib.Settings.log_path, remaining_urls)
        except Exception as err:
            log.info('Errog deleting posts!', exc_info=True)
            sys.exit(1)


def scrape_urls(driver, file_size):
    """scrape for new url's to delete if current list is empty"""
    if (file_size == 0):
        log.info('file empty, going to scroll')
        source_data = scroll_to_end(browser=driver)
        URLS = parse_href(source_data)
        write_to_archive(ib.Settings.log_path, URLS)


def main():
    ib.start_end_log(__file__)
    driver = ib.login_with_cookies()
    scrape_urls(driver, file_size=os.stat(ib.Settings.log_path).st_size)
    delete_posts(browser=driver)
    ib.save_cookies(driver)
    driver.quit()


if __name__ == '__main__':
    main()
    ib.start_end_log(__file__, end_log=True)