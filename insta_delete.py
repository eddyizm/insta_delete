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

# store urls to delete later
log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
#ig_html = r'C:\Users\eddyizm\Downloads\eddyizm.html'
logintext = "C:\\Users\\eddyizm\\Desktop\\Work\\login.txt"
URLS = []
post_counter = 500

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
        browser = webdriver.Chrome()
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
    browser = webdriver.Chrome()
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
        mobile_emulation = { "deviceName": "Pixel 2" }
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument("window-size=500,800")
        browser = webdriver.Chrome(chrome_options=options)
        browser.get("https://www.instagram.com/accounts/login/")
        stime(3)
        f = open (logintext, 'r')
        login = f.read().splitlines()
        f.close()
        insta_username = login[0]
        insta_password = login[1]
            
        eUser = browser.find_elements_by_xpath(
            "//input[@name='username']")
        stime(4)
        ActionChains(browser).move_to_element(eUser[0]). \
            click().send_keys(insta_username).perform()
        stime(4)
        ePass = browser.find_elements_by_xpath(
            "//input[@name='password']")
        stime(4)
        ActionChains(browser).move_to_element(ePass[0]). \
            click().send_keys(insta_password).perform()

        
        stime(6)
        login_button = browser.find_element_by_xpath(
            "//button[text()='Log in']")
            #"//form/span/button[text()='Log in']")
                     
        ActionChains(browser).move_to_element(login_button).click().perform()
        stime(10)
            
        links = OpenLog()
        new_file = []
        deleted_urls = []
        counter = 15
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
                    options_button = browser.find_element_by_xpath(
                        "//span[@aria-label='More options']")
                    ActionChains(browser).move_to_element(options_button).click().perform()                
                    stime(10)
                    delete_button = browser.find_element_by_xpath(
                        "//button[text()='Delete']")
                    ActionChains(browser).move_to_element(delete_button).click().perform()
                    stime(10)
                    confirm_delete = browser.find_element_by_xpath(
                        "//button[text()='Delete']")
                    ActionChains(browser).move_to_element(confirm_delete).click().perform()
                    stime(10)
                    deleted_urls.append(new_file[counter])
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
    print ('file size: '+str(file_size))
    if (os.stat(log_path).st_size == 0):
        print ('file empty, going to scroll')
        source_data = scroll_to_end()
        URLS = parse_href(source_data)
        WriteToArchive(log_path, URLS)    

    # # manually load html file
    # URLS = parse_href( open(ig_html, 'r',  encoding= 'utf-8') ) 
    # WriteToArchive(log_path, URLS)
    if profile_post_min(post_counter):
        login_to_site()
    print ('----------------------------------------------------------------------------------------------------- ')
    print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ('--------------------------------------- end session ------------------------------------------------- ')
    print ('----------------------------------------------------------------------------------------------------- ')

    sys.exit()