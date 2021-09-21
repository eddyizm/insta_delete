# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import time
import os
import sys
import json

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

if os.name == 'nt':
    log_path = settings['windows']['log_path']
    # log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
    firefoxPath= settings['windows']['firefoxPath']
else:
    firefoxPath="env/geckodriver"
    # logintext = "env/login.txt"
    # log_path = 'env/media_urls.txt'
    linux = True


def stime(seconds):
    return time.sleep(seconds)


def OpenLog():
    with open(log_path, 'r', encoding= 'utf-8') as g:
        lines = g.read().splitlines()
        return (lines)


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


def profile_post_min(counter):
    try:
        browser = webdriver.Firefox(executable_path=firefoxPath)
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        browser.get("https://www.instagram.com/eddyizm")
        print ('checking post count limit currently set at: '+str(counter))
        post_count = ''
        stime(10)
        links = BeautifulSoup(browser.page_source, "html.parser", parse_only=SoupStrainer('a'))
        browser.close()
        for x in links:
            t = x.get('href')
            if 'profile_posts' in t:
                post_count = x.text.replace(' posts','')
                print (post_count)
        if int(post_count.replace(',','')) > counter:
            return True
        else:
            print ('count mininum reached.')
            return False
    except ValueError as err:
        print ('profile_post_min :ERROR:')
        print (err)
        return False

def scroll_to_end():
    browser = webdriver.Firefox(executable_path=firefoxPath)
    # if linux:
    #     browser = webdriver.Firefox(executable_path=firefoxPath)
    # else:
    #     browser = webdriver.Firefox()        
    get_html = None
    print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ('scrolling profile to get more urls')
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
        print ('scrolled down: '+str(count)+' times!')
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as err:
        print (err)
        browser.close()
    return get_html


def login_to_site():
    try:
        print ('logging in as mobile device to delete')
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user_agent = "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
        profile = webdriver.FirefoxProfile() 
        profile.set_preference("general.useragent.override", user_agent)
        browser = webdriver.Firefox(firefox_profile = profile, executable_path=firefoxPath)
        # if linux:
        #     browser = webdriver.Firefox(firefox_profile = profile, executable_path=firefoxPath)
        # else:
        #     browser = webdriver.Firefox(firefox_profile = profile)
        browser.set_window_size(360,640)
        browser.get("https://www.instagram.com/accounts/login/")
        stime(10)
        # f = open (logintext, 'r')
        # login = f.read().splitlines()
        # f.close()
        # insta_username = login[0]
        # insta_password = login[1]
        eUser = browser.find_elements_by_xpath(
            "//input[@name='username']")
        stime(10)
        ActionChains(browser).move_to_element(eUser[0]). \
            click().send_keys(insta_username).perform()
        stime(10)
        ePass = browser.find_elements_by_xpath(
            "//input[@name='password']")
        stime(10)
        ActionChains(browser).move_to_element(ePass[0]). \
            click().send_keys(insta_password).perform()

        stime(10)
        login_button = browser.find_element_by_xpath(
            "//*[contains(text(), 'Log In')]")
            #"//button[text()='Log In']")
            #"//form/span/button[text()='Log In']")
                     
        ActionChains(browser).move_to_element(login_button).click().perform()
        stime(10)
            
        links = OpenLog()
        new_file = []
        deleted_urls = []
        counter = 10
        for l in links:
            if l.startswith('https://www.instagram.com/p/'):
                new_file.append(l)
        
        print ('length of file: '+str(len(new_file)))
        if (counter >= len(new_file)):
            counter = (len(new_file) - 1)
        
        print ('counter: '+str(counter))
        
        try:
            print ('DELETING POSTS!')
            print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            while (counter > -1):
                browser.get(new_file[counter])
                stime(10)
                
                if ("Sorry, this page isn't available." in browser.page_source):
                    deleted_urls.append(new_file[counter])
                    print ('URL not found, removing from list')
                    counter -= 1
                else:                
                    # used this to debug and find html changes.
                    # checkhtml = BeautifulSoup(browser.page_source, "html.parser")
                    # with open('debug.html', 'w', encoding='utf-8') as w:
                    #     w.write(checkhtml.prettify())
                    options_button = browser.find_element_by_xpath(
                            "//div[@class='MEAGs']//*[@aria-label='More options']")
                    ActionChains(browser).move_to_element(options_button).click().perform()                
                    stime(10)
                    delete_button = browser.find_element_by_xpath(
                        "//button[text()='Delete']")
                    ActionChains(browser).move_to_element(delete_button).click().perform()
                    stime(10)
                    confirm_delete = browser.find_element_by_xpath(
                        "//button[text()='Delete']")
                    ActionChains(browser).move_to_element(confirm_delete).click().perform()
                    deleted_urls.append(new_file[counter])
                    stime(10)
                    print ('POST DELETED: '+new_file[counter])
                    counter -= 1

            l3 = [x for x in new_file if x not in deleted_urls]
            print ('while loop done and exited successfully')
            print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            WriteToArchive(log_path, l3)	    
            browser.close()

        except Exception as err:
            print (err)
            browser.close()
            sys.exit()
    
    except Exception as err:
        print (err)        


if __name__ == '__main__':
    print ('----------------------------------------------------------------------------------------------------- ')
    print ('--------------------------------------- new session ------------------------------------------------- ')
    print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ('----------------------------------------------------------------------------------------------------- ')
    file_size = os.stat(log_path).st_size
    print ('file size: '+ str(file_size))
    if (os.stat(log_path).st_size == 0):
        print ('file empty, going to scroll')
        source_data = scroll_to_end()
        URLS = parse_href(source_data)
        WriteToArchive(log_path, URLS)    
    # # manually load html file
    # URLS = parse_href( open(ig_html, 'r',  encoding= 'utf-8') ) 
    if profile_post_min(post_counter):
        login_to_site()
    print ('----------------------------------------------------------------------------------------------------- ')
    print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ('--------------------------------------- end session ------------------------------------------------- ')
    print ('----------------------------------------------------------------------------------------------------- ')

    sys.exit()