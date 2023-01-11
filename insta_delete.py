# -*- coding: UTF-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, SoupStrainer
import os
import sys
import logging

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
    ib.stime
    delete = browser.find_element(by=By.XPATH, value="//button[text()='Delete']")
    ib.click_element(browser, delete, 'delete')


def profile_post_min(counter, browser):
    # TODO this function is currently not working and thus returning True regardless
    result = False
    try:
        browser.get(f"https://www.instagram.com/{ib.Settings.insta_username}")
        log.info(f'checking post count limit currently set at: {counter}')
        post_count = ''
        ib.stime()
        links = BeautifulSoup(browser.page_source, "html.parser", parse_only=SoupStrainer('a'))
        for x in links:
            t = x.get('href')
            if 'posts' in t:
                post_count = x.text.replace(' posts','')
                log.info(f'post count: {post_count}')

        if len(post_count) > 0 and int(post_count.replace(',','')) > counter:
            result = True
        else:
            log.info('count mininum reached.')
            result = False
    except ValueError as err:
        log.info('profile_post_min :ERROR:')
        log.info(err)
    finally:
        return True


def scroll_to_end(browser):
    get_html = None
    log.info('scrolling profile to get more urls')
    try:
        browser.get(f"https://www.instagram.com/{ib.Settings.insta_username}")
        match = False
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        count = 0
        while(match==False):
            lastCount = lenOfPage
            ib.stime
            log.info('scrolling ...')    
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count += 1
            # added count to ensure only older images get picked up. 
            if (lastCount==lenOfPage) and (count > 25):
                match=True
                
        get_html = browser.page_source                       
        browser.close()
        log.info('scrolled down: '+str(count)+' times!')
    except Exception as err:
        log.info('error scrolling to end', exc_info=True)
        browser.close()
    return get_html


def delete_posts(browser):
        deleted_urls = []
        new_file = open_archive()
        counter = (len(new_file) - 1) if (10 >= len(new_file)) else 10
        log.info('number of posts to delete: '+str(counter))
        try:
            log.info('DELETING POSTS!')
            while (counter > -1):
                log.info(f'getting new url: {new_file[counter]}')
                browser.get(new_file[counter])
                ib.stime
                if ("Sorry, this page isn't available." in browser.page_source):
                    deleted_urls.append(new_file[counter])
                    log.info('URL not found, removing from list')
                    counter -= 1
                else:                
                    log.info(f'finding 3 dot options...')
                    more_options = browser.find_elements(by=By.XPATH, value="//*[local-name()='svg' and @aria-label='More options']")[1]
                    ib.stime
                    ib.click_element(browser, more_options, 'more options')
                    find_delete_button(browser)
                    find_delete_button(browser)
                    deleted_urls.append(new_file[counter])
                    log.info('POST DELETED: '+new_file[counter])
                    counter -= 1

            remaining_urls = [x for x in new_file if x not in deleted_urls]
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
    driver.close()

if __name__ == '__main__':
    main()
    ib.start_end_log(__file__, end_log=True)