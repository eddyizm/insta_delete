from selenium import webdriver
import time

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
#start session
browser = webdriver.Chrome()
browser.get('https://login.frontlineeducation.com/login?signin=eb9838bc56c4c37d308b52ada3dacb6e&productId=ABSMGMT&clientId=ABSMGMT#/login')  

user = getFrontlineEdu(wtext)
eUser = browser.find_element_by_id('Username')
ePass = browser.find_element_by_id("Password")

eUser.send_keys(user[86])
stime(2)
ePass.send_keys(user[87])
stime(5)

'''
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
'''
# options for webdriver
''' 
    # added options to disable notification pop up
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    #start session
    browser = webdriver.Chrome(chrome_options=options)
'''    