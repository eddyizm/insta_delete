from selenium import webdriver
import time

# globals
logintext = "C:/Users/cervantes/Downloads/slogin.txt"
wtext = "Y:/My Documents/Tools/temp.md"

# wait function
def stime(seconds):
    return time.sleep(seconds)
# message to test
def baseMessage():
    tstamp = time.strftime("%H:%M:%S")
    m = "Hello, I am Eduardo and it is "+tstamp+".\n I am a mexican bot, not a russian one"
    return m
# function to get fb credentials from text file 
def getFBcredentials(textfile):
    with open(logintext) as f:
        return f.read().splitlines()
def LoginToFB():        
    # get login info
    user = getFBcredentials(logintext)

    # added options to disable notification pop up
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)

    #start session
    browser = webdriver.Chrome(chrome_options=options)

    browser.get('https://facebook.com')       

    assert "Facebook" in browser.title
    #get login elements 
    elemUser = browser.find_element_by_id("email")
    elemPass = browser.find_element_by_id("pass")
    btnLogin = browser.find_element_by_id("loginbutton")

    elemUser.send_keys(user[0])
    stime(2)
    elemPass.send_keys(user[1])
    stime(5)
    btnLogin.submit()
# successfully logged in. Let's look for the wall post feature. 
# no luck. will try again later when Leia stops peeing all over the house.
def getADP(textfile):
    with open(textfile) as f:
        return f.read().splitlines()
#start session
browser = webdriver.Chrome()

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
browser.close()
