from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import youtube_dl

# globals
logintext = "C:/Users/cervantes/Downloads/slogin.txt"
#wtext = "Y:/My Documents/Tools/temp.md"
wtext = "C:/Users/eddyizm/Desktop/Work/temp.md"
# wait function
def stime(seconds):
    return time.sleep(seconds)
def getADP(textfile):
    with open(textfile) as f:
        return f.read().splitlines()
def getFrontlineEdu(textfile):
    with open(textfile) as f:
        return f.read().splitlines()
<<<<<<< HEAD
#start session
browser = webdriver.Chrome()
# browser.get('https://login.frontlineeducation.com/login?signin=eb9838bc56c4c37d308b52ada3dacb6e&productId=ABSMGMT&clientId=ABSMGMT#/login')  

# user = getFrontlineEdu(wtext)
# eUser = browser.find_element_by_id('Username')
# ePass = browser.find_element_by_id("Password")

# eUser.send_keys(user[86])
# stime(2)
# ePass.send_keys(user[87])
# stime(5)
=======

try:

    #start session
    browser = webdriver.Chrome()
    
    browser.get('https://login.frontlineeducation.com/login?signin=eb9838bc56c4c37d308b52ada3dacb6e&productId=ABSMGMT&clientId=ABSMGMT#/login')  

    user = getFrontlineEdu(wtext)
    # wait for page
    stime(20)
    # WebDriverWait(self.driver, 10).until(lambda s: s.find_element_by_id("Username").is_displayed())
    eUser = browser.find_element_by_id('Username')
    ePass = browser.find_element_by_id("Password")

    eUser.send_keys(user[86])
    stime(2)
    ePass.send_keys(user[87])
    stime(5)
    btnLogin = browser.find_element_by_id('qa-button-login')
    btnLogin.submit()
    #WebDriverWait(browser, 10).until(lambda s: s.find_element_by_id("availableJobs").is_displayed())
    stime(15)
    #f = urllib.request.urlopen(browser.current_url)
        
    #soup = BeautifulSoup(f.read(), 'html.parser')
    #print (soup)
    browser.quit()


except TimeoutException:
    print('Timed out waiting for page to load')
    browser.quit()



>>>>>>> 3ec61f668a2cbc3a9e3d4781fc55e445a7aeaa5e

browser.get('https://workforcenow.adp.com/public/index.htm')  
assert "ADP" in browser.title

elemUser = browser.find_element_by_class_name("input1")
elemPass = browser.find_element_by_class_name("input2")
btnLogin = browser.find_element_by_id("portal.login.logIn")

user = getADP(wtext)
elemUser.send_keys(user[37])
stime(2)
elemPass.send_keys(user[38])
stime(5)
btnLogin.submit()
stime(30)
browser.close()

# options for webdriver
''' 
    # added options to disable notification pop up
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    #start session
    browser = webdriver.Chrome(chrome_options=options)
'''    