# insta_delete
Selenium, BS4 powered script to delete old instagram posts.

Working with selenium can be challenging if you have no previous experience with it. Part of this project was for me to get more comfortable using selenium on an ever changing UI. 

## Prerequisites

Download ```chromedriver``` for your system [from here](https://sites.google.com/a/chromium.org/chromedriver/downloads). The script uses chromedriver after setting it in the path variables. Otherwise you can specify the specific location of the executable. 

If chromedriver is not specified in your environ, replace the code
```
browser = webdriver.Chrome()
```
with 
```
browser = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
```

See the getting started page for more help: http://chromedriver.chromium.org/getting-started


## Installation

    pip install -r requirements.txt

## Usage

I set up variables to store the URLS and account information. 

    log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
    logintext = "C:\\Users\\eddyizm\\Desktop\\Work\\login.txt"

These will need to be replaced with local paths for your system. 
The login.txt should be split into two lines:

    USERNAME
    PASSWORD

Other wise you can comment out the file open portion and replace the ```login[0]``` values with your credentials:

    #f = open (logintext, 'r')
    #login = f.read().splitlines()
    #f.close()
    insta_username = USERNAME
    insta_password = PASSWORD

