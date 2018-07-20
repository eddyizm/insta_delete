# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
import time

# store urls to delete later
log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
ig_html = r'C:\Users\eddyizm\Downloads\eddyizm.html'
logintext = "C:\\Users\\eddyizm\\Desktop\\Work\\login.txt"

def stime(seconds):
    return time.sleep(seconds)

def OpenLog():
    with open(log_path, 'r', encoding= 'utf-8') as g:
        lines = g.read().splitlines()
        return (lines)

def WriteToArchive(log, data):
     with open(log, 'w', encoding= 'utf-8') as f:
         for d in data:
             f.write(str(d)+'\n')

def parse_href(data):
    url_list = []
    with open(data, encoding= 'utf-8') as fp:
        for link in BeautifulSoup(fp, "html.parser", parse_only=SoupStrainer('a') ):
            if link.has_attr('href'):
                t = link.get('href')
                if t is not None:
                    url_list.append(t)
                    print (t)
        return url_list            

# # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  
# # It will continue to do this until the page stops loading new data.
def scroll_to_end():
    browser = webdriver.Chrome()
    browser.get("https://www.instagram.com/eddyizm")
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    count = 0
    while(match==False):
            lastCount = lenOfPage
            time.sleep(10)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count += 1
            print (count)
            if lastCount==lenOfPage:
                match=True
                print (count)
    source = browser.page_source()                       
    browser.close()
    return source

def delete_posts(browser_object):
    links = OpenLog()
    new_file = []
    deleted_urls = []
    counter = 10
    for l in links:
        if l.startswith('https://www.instagram.com/p/'):
            new_file.append(l)
            
            #browser_object
    try:
        while counter > 0:
            browser_object.get(new_file[counter])
            stime(10)
            options_button = browser_object.find_element_by_xpath(
                "//span[text()='More options']")
            ActionChains(browser_object).move_to_element(options_button).click().perform()                
            stime(3)
            delete_button = browser_object.find_element_by_xpath(
                "//button[text()='Delete']")
            ActionChains(browser_object).move_to_element(delete_button).click().perform()
            stime(10)
            confirm_delete = browser_object.find_element_by_xpath(
                "//button[text()='Delete']")
            ActionChains(browser_object).move_to_element(confirm_delete).click().perform()
            stime(10)
            deleted_urls.append(new_file[counter])
            counter -= 1

        l3 = [x for x in new_file if x not in deleted_urls]
        WriteToArchive(log_path, l3)	    

    except:
        pass

def login_to_site():
    mobile_emulation = { "deviceName": "Pixel 2" }
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    #options.add_experimental_option()
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
    stime(1)
    ActionChains(browser).move_to_element(eUser[0]). \
        click().send_keys(insta_username).perform()
    stime(1)
    ePass = browser.find_elements_by_xpath(
        "//input[@name='password']")
    stime(2)
    ActionChains(browser).move_to_element(ePass[0]). \
        click().send_keys(insta_password).perform()

    
    stime(5)
    login_button = browser.find_element_by_xpath(
        "//form/span/button[text()='Log in']")
    # login_elem = browser.find_elements_by_xpath(
    #     "//*[contains(text(), 'Log in')]")    
    ActionChains(browser).move_to_element(login_button).click().perform()
    stime(10)
    # break this into the delete function
    
    links = OpenLog()
    new_file = []
    deleted_urls = []
    counter = 10
    for l in links:
        if l.startswith('https://www.instagram.com/p/'):
            new_file.append(l)
    
    if (counter > len(new_file)):
        counter = len(new_file)
    
    try:
        print ('in try block')
        while (counter > 0):
            print (new_file[counter])
            browser.get(new_file[counter])
            stime(10)
            options_button = browser.find_element_by_xpath(
                "//span[text()='More options']")
            ActionChains(browser).move_to_element(options_button).click().perform()                
            stime(3)
            delete_button = browser.find_element_by_xpath(
                "//button[text()='Delete']")
            ActionChains(browser).move_to_element(delete_button).click().perform()
            stime(10)
            confirm_delete = browser.find_element_by_xpath(
                "//button[text()='Delete']")
            ActionChains(browser).move_to_element(confirm_delete).click().perform()
            stime(10)
            deleted_urls.append(new_file[counter])
            counter -= 1

        l3 = [x for x in new_file if x not in deleted_urls]
        WriteToArchive(log_path, l3)	    
        browser.close()

    except:
        browser.close()
   
if (os.stat(log_path).st_size == 0:
    source_data = scroll_to_end()
    URLS = parse_href(source_data)
    WriteToArchive(log_path, URLS)    

login_to_site()

