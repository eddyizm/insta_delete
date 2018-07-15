from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json, requests

# store urls to delete later
log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'

# this part will be to scroll to the end and record urls
browser = webdriver.Chrome()
browser.get("https://www.instagram.com/eddyizm")
# Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  
# It will continue to do this until the page stops loading new data.
lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

# Now that the page is fully scrolled, grab the source code.
source_data = browser.page_source

# Throw your source into BeautifulSoup and start parsing!
bs_data = bs(source_data)

def writeToLog(log):
    with open(log, 'w') as g:
        for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                #t = parseUrl.CheckUrl(link['href'])
                if t is not None:
                    g.write(t +'\n')

#writeToLog(log_path)                    