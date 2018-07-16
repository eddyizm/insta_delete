# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
import time

def WriteToArchive(log, data):
     with open(log, 'w', encoding= 'utf-8') as f:
         for d in data:
             f.write(str(d)+'\n')

# store urls to delete later
log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
ig_html = r'C:\Users\eddyizm\Downloads\eddyizm.html'

# this part will be to scroll to the end and record urls

# browser = webdriver.Chrome()
# browser.get("https://www.instagram.com/eddyizm")
# # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  
# # It will continue to do this until the page stops loading new data.

# lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# match=False
# while(match==False):
#         lastCount = lenOfPage
#         time.sleep(10)
#         lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#         if lastCount==lenOfPage:
#             match=True
            
# Now that the page is fully scrolled, grab the source code.
#source_data = browser.page_source


URLS = []

#soup = BeautifulSoup(source_data, parse_only=SoupStrainer('a'))
with open(ig_html, encoding= 'utf-8') as fp:
    for link in BeautifulSoup(fp, "html.parser", parse_only=SoupStrainer('a') ):
        if link.has_attr('href'):
            t = link.get('href')
            if t is not None:
              URLS.append(t)
              print (t)    #if (t[0:2] == '/p/'):
    
WriteToArchive(log_path, URLS)
#browser.close()
# now to read the file and open the URL, navigate to delete button and remove post,
# move to new url, wait 10 minutes, delete and loop through a few.

def OpenLog():
    with open(log_path, 'r', encoding= 'utf-8') as g:
        lines = g.read()
        return (lines)

browser = webdriver.Chrome()
pattern = 'https://www.instagram.com/p/'


browser.get("https://www.instagram.com/eddyizm")