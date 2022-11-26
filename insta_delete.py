# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import time
import os
import sys
import json
import logging as log

linux = False
URLS = []
post_counter = 50
CONFIG = r"C:\Users\eddyizm\HP\config.json"

def get_keys():
    with open(CONFIG, 'r') as myfile:
        keys = myfile.read()
        return json.loads(keys)

settings = get_keys()
insta_username = settings['instagram']['login']
insta_password = settings['instagram']['pass']
log_path = settings['windows']['log_path']
app_log = settings['windows']['app_log']
firefoxPath= settings['windows']['firefoxPath']
profile_path = settings['windows']['profile_path']
    
handlers = [log.FileHandler(app_log), log.StreamHandler()]
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', handlers = handlers, level=log.INFO)


def stime():
    return time.sleep(5)


def OpenLog():
    with open(log_path, 'r', encoding= 'utf-8') as g:
        lines = g.read().splitlines()
        return (lines)


def dump_html_to_file(driver):
    ''' used this to debug and find html changes. '''
    checkhtml = BeautifulSoup(driver.page_source, "html.parser")
    with open('debug.html', 'w', encoding='utf-8') as w:
        w.write(checkhtml.prettify())


def WriteToArchive(log, data):
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


def profile_post_min(counter, browser):
    # TODO this function is currently not working and thus returning True regardless
    result = False
    try:
        browser.get("https://www.instagram.com/eddyizm")
        log.info(f'checking post count limit currently set at: {counter}')
        post_count = ''
        stime()
        links = BeautifulSoup(browser.page_source, "html.parser", parse_only=SoupStrainer('a'))
        # dump_html_to_file(driver=browser)
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
        browser.get("https://www.instagram.com/eddyizm")
        #match = check_posts(browser.page_source, post_counter) 
        match = False
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        count = 0
        while(match==False):
            lastCount = lenOfPage
            time.sleep(10)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count += 1
            # added count to ensure only older images get picked up. 
            if (lastCount==lenOfPage) and (count > 25):
                match=True
                
        get_html = browser.page_source                       
        browser.close()
        log.info('scrolled down: '+str(count)+' times!')
        log.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as err:
        log.info(err)
        browser.close()
    return get_html


def login_to_site():
    try:
        log.info('logging in as mobile device to delete')
        user_agent = "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
        # profile = webdriver.FirefoxProfile() 
        # profile.set_preference("general.useragent.override", user_agent)
        options=Options()
        options.set_preference('profile', profile_path)
        service = Service(firefoxPath)
        browser = webdriver.Firefox(service=service, options=options)
        # browser = webdriver.Firefox(firefox_profile = profile, executable_path=firefoxPath)
        browser.set_window_size(360,640)
        browser.get("https://www.instagram.com/accounts/login/")
        stime()
        eUser = browser.find_element(by=By.XPATH, value="//input[@name='username']")
        log.info(f'found username element: {eUser}')
        stime()
        ActionChains(browser).move_to_element(eUser). \
            click().send_keys(insta_username).perform()
        stime()
        ePass = browser.find_element(by=By.XPATH, value="//input[@name='password']")
        stime()
        ActionChains(browser).move_to_element(ePass). \
            click().send_keys(insta_password).perform()

        stime()
        login_button = browser.find_element(by=By.XPATH, value="//*[contains(text(), 'Log In')]")
            #"//button[text()='Log In']")
            #"//form/span/button[text()='Log In']")
                     
        ActionChains(browser).move_to_element(login_button).click().perform()
        stime()
        return browser
    except Exception as err:
        log.info(err)
        browser.close()
        sys.exit(1)


def delete_posts(browser):
        links = OpenLog()
        new_file = []
        deleted_urls = []
        counter = 10
        for l in links:
            if l.startswith('https://www.instagram.com/p/'):
                new_file.append(l)
        
        log.info('length of file: '+str(len(new_file)))
        if (counter >= len(new_file)):
            counter = (len(new_file) - 1)
        
        log.info('number of posts to delete: '+str(counter))
        
        try:
            log.info('DELETING POSTS!')
            while (counter > -1):
                log.info(f'getting new url: {new_file[counter]}')
                browser.get(new_file[counter])
                stime()
                
                if ("Sorry, this page isn't available." in browser.page_source):
                    deleted_urls.append(new_file[counter])
                    log.info('URL not found, removing from list')
                    counter -= 1
                else:                
                    options_button = browser.find_element(by=By.XPATH, value="//div[@class='_aasm']//*[@aria-label='More options']")
                    ActionChains(browser).move_to_element(options_button).click().perform()                
                    stime()
                    delete_button = browser.find_element(by=By.XPATH, value="//button[text()='Delete']")
                    ActionChains(browser).move_to_element(delete_button).click().perform()
                    stime()
                    confirm_delete = browser.find_element(by=By.XPATH, value="//button[text()='Delete']")
                    ActionChains(browser).move_to_element(confirm_delete).click().perform()
                    deleted_urls.append(new_file[counter])
                    stime()
                    log.info('POST DELETED: '+new_file[counter])
                    counter -= 1

            l3 = [x for x in new_file if x not in deleted_urls]
            log.info('while loop done and exited successfully')
            log.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            WriteToArchive(log_path, l3)	    
            browser.close()

        except Exception as err:
            log.info(err)
            browser.close()
            sys.exit(1)
    

if __name__ == '__main__':
    log.info('----------------------------------------------------------------------------------------------------- ')
    log.info('--------------------------------------- new session ------------------------------------------------- ')
    log.info('----------------------------------------------------------------------------------------------------- ')
    file_size = os.stat(log_path).st_size
    log.info('file size: '+ str(file_size))
    agent = login_to_site()
    if (os.stat(log_path).st_size == 0):
        log.info('file empty, going to scroll')
        source_data = scroll_to_end(browser=agent)
        URLS = parse_href(source_data)
        WriteToArchive(log_path, URLS)    
    # # manually load html file
    # URLS = parse_href( open(ig_html, 'r',  encoding= 'utf-8') ) 
    # if profile_post_min(counter=post_counter, browser=agent):
    delete_posts(browser=agent)
    log.info('----------------------------------------------------------------------------------------------------- ')
    log.info('--------------------------------------- end session ------------------------------------------------- ')
    log.info('----------------------------------------------------------------------------------------------------- ')

    sys.exit(0)