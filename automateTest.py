from selenium import webdriver

def getFBcredentials(textfile):
    with open(logintext) as f:
        return f.read().splitlines()
# get login info
logintext = "C:/Users/cervantes/Downloads/slogin.txt"
user = getFBcredentials(logintext)

#start session
browser = webdriver.Chrome()
browser.get('https://facebook.com')       

assert "Facebook" in browser.title
#get login elements 
elemUser = browser.find_element_by_id("email")
elemPass = browser.find_element_by_id("pass")
btnLogin = browser.find_element_by_id("loginbutton")

elemUser.send_keys(user[0])
elemPass.send_keys(user[1])
btnLogin.submit()

browser.close()
# browser = webdriver.Chrome()
# browser.get('http://seleniumhq.org')    